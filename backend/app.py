from flask import Flask, request, session
import secrets
from models import db,User, Admin, ParkingLot, ParkingSpot, Reservation
from flask_migrate import Migrate
from flask import jsonify
from werkzeug.security import check_password_hash
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from flask_caching import Cache
from flask import Flask
from celery_config import make_celery
from datetime import timezone
from datetime import datetime, timedelta
from celery.result import AsyncResult
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)   
app.secret_key = secrets.token_hex(16)


# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///C:/Users/HP/Desktop/vehicle_parking.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration for Celery
celery = make_celery(app)

# Initialize the database
db.init_app(app)
m = Migrate(app,db)

# Cache configuration
cache = Cache(app, config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': "redis://localhost:6379/0"})
cache.init_app(app)

# CORS configuration
CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})

# Create tables (Only needed on the first run)
# with app.app_context():
#     try:
#         db.create_all()
#         print("Tables created successfully")
#     except Exception as e:
#         print(f"Error creating tables: {e}")


# ======================COMMON ROUTES=======================     
@app.route('/')
def home():
    return "Welcome to the Home Page!"

session= {}
@app.route('/api/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    admin = Admin.query.filter_by(email=email).first()
    if admin and check_password_hash(admin.password, password):
        session['admin_id'] = admin.admin_id
        return jsonify({'success': True, 'role': 'admin', 'message': 'Login successful!'}), 200

    customer = User.query.filter_by(email=email).first()
    if customer and check_password_hash(customer.password, password):
        session['customer_id'] = customer.user_id
        return jsonify({'success': True, 'role': 'customer', 'message': 'Login successful!'}), 200

    return jsonify({'success': False, 'message': 'Invalid credentials. Please try again.'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('customer_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200


# ======================ADMIN ROUTES=======================

@app.route('/api/clear-lot-cache', methods=['GET'])
def clear_lot_cache():
    cache.delete_memoized(get_all_parking_lots)
    return jsonify({"message": "Lot cache cleared!"})

import time
@app.route('/api/get_all_parking_lots', methods=['GET'])
@cache.cached(timeout=60)
def get_all_parking_lots():
    start=time.time()
    lots = ParkingLot.query.all()
    result = []
    for lot in lots:
        slots = ParkingSpot.query.filter_by(parking_lot_id=lot.parking_lot_id).all()
        slot_data = [
            {
                "parking_spot_id": spot.parking_spot_id,
                "status": spot.status
            }
            for spot in slots
        ]
        occupied_count = sum(1 for spot in slots if spot.status == 'O')
        result.append({
            "id": lot.parking_lot_id,
            "occupied": occupied_count,
            "total": lot.number_of_spots,
            "slots": slot_data
        })
    print(f"Time taken to fetch parking lots: {time.time() - start} seconds")
    return jsonify(result)



@app.route('/api/add_parking_lot', methods=['POST'])
def add_parking_lot():
    data = request.json
    try:
        new_lot = ParkingLot(
            prime_location_name=data['prime_location_name'],
            address=data['address'],
            pincode=data['pincode'],
            price=data['price'],
            number_of_spots=data['number_of_spots'],
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(new_lot)
        db.session.commit()

        # create empty parking spots
        for _ in range(new_lot.number_of_spots):
            spot = ParkingSpot(parking_lot_id=new_lot.parking_lot_id, status='A')
            db.session.add(spot)
        db.session.commit()

        return jsonify({"message": "Parking lot added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/get_parking_lot/<int:parking_lot_id>', methods=['GET'])
def get_parking_lot(parking_lot_id):
    lot = ParkingLot.query.get(parking_lot_id)
    if lot:
        return jsonify({
            'parking_lot_id': lot.parking_lot_id,
            'prime_location_name': lot.prime_location_name,
            'address': lot.address,
            'pincode': lot.pincode,
            'price': lot.price,
            'number_of_spots': lot.number_of_spots
        })
    else:
        return jsonify({'error': 'Not found'}), 404

@app.route('/api/update_parking_lot/<int:parking_lot_id>', methods=['PUT'])
def update_parking_lot(parking_lot_id):
    data = request.json
    lot = ParkingLot.query.get(parking_lot_id)
    if not lot:
        return jsonify({'error': 'Parking lot not found'}), 404

    lot.prime_location_name = data['prime_location_name']
    lot.address = data['address']
    lot.pincode = data['pincode']
    lot.price = data['price']
    lot.number_of_spots = data['number_of_spots']

    db.session.commit()
    return jsonify({'message': 'Updated successfully'})


@app.route('/api/admin_delete_service/<int:id>', methods=['DELETE'])
def delete_parking_lot(id):
    lot = ParkingLot.query.get(id)
    if not lot:
        return jsonify({'error': 'Parking lot not found'}), 404

    db.session.delete(lot)
    db.session.commit()
    return jsonify({'message': 'Parking lot deleted successfully'})

@app.route('/api/admin_users', methods=['GET'])
def admin_users():
    try:
        users = User.query.all()
        user_list = [
            {
                "id": user.user_id,
                "email": user.email,
                "full_name": user.full_name,
                "address": user.address,
                "pin_code": user.pincode
            }
            for user in users
        ]
        return jsonify({"users": user_list}), 200

    except Exception as e:
        app.logger.error(f"Error fetching users: {e}")
        return jsonify({"error": "Unable to fetch users"}), 500
    

@app.route('/api/admin_search', methods=['GET'])
def admin_search():
    by = request.args.get('by')
    text = request.args.get('text')

    if not by or not text:
        return jsonify({'error': 'Missing search parameters'}), 400

    results = []

    try:
        if by == 'user_id':
            
            user = User.query.get(int(text))
            if not user:
                return jsonify({'results': []}), 200

            for res in user.reservations:
                spot = res.parking_spot
                lot = spot.parking_lot
                slots = [s.status for s in lot.spots]
                occupied = sum(1 for s in slots if s == 'O')
                results.append({
                    'parking_id': lot.parking_lot_id,
                    'location_name': lot.prime_location_name,
                    'occupied': occupied,
                    'capacity': lot.number_of_spots,
                    'slots': slots
                })

        elif by == 'location':
            
            lots = ParkingLot.query.filter(
                ParkingLot.prime_location_name.ilike(f'%{text}%')
            ).all()
            for lot in lots:
                slots = [s.status for s in lot.spots]
                occupied = sum(1 for s in slots if s == 'O')
                results.append({
                    'parking_id': lot.parking_lot_id,
                    'location_name': lot.prime_location_name,
                    'occupied': occupied,
                    'capacity': lot.number_of_spots,
                    'slots': slots
                })

        elif by == 'parking_id':
            
            spot = ParkingSpot.query.get(int(text))
            if spot:
                lot = spot.parking_lot
                slots = [s.status for s in lot.spots]
                occupied = sum(1 for s in slots if s == 'O')
                results.append({
                    'parking_id': lot.parking_lot_id,
                    'location_name': lot.prime_location_name,
                    'occupied': occupied,
                    'capacity': lot.number_of_spots,
                    'slots': slots
                })

        else:
            return jsonify({'error': 'Invalid search parameter'}), 400

        return jsonify({'results': results}), 200

    except ValueError:
        return jsonify({'error': 'Invalid ID format'}), 400
    except Exception as e:
        app.logger.error(f"admin_search error: {e}")
        return jsonify({'error': 'Server error'}), 500


@app.route('/api/admin_stats/revenue', methods=['GET'])
@cache.cached(timeout=600)
def stats_revenue():
    stats = []
    lots = ParkingLot.query.all()
    for lot in lots:
        total = db.session.query(
          db.func.sum(Reservation.parking_cost)
        ).join(ParkingSpot).filter(
          ParkingSpot.parking_lot_id == lot.parking_lot_id
        ).scalar() or 0.0

        stats.append({
          'parking_id': lot.parking_lot_id,
          'revenue': total
        })
    return jsonify(stats), 200


@app.route('/api/admin_stats/occupancy', methods=['GET'])
@cache.cached(timeout=600)
def stats_occupancy():
    total_spots = ParkingSpot.query.count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()
    return jsonify({
        'available': total_spots - occupied_spots,
        'occupied': occupied_spots
    }), 200


@app.route('/api/admin/profile', methods=['GET'])
def get_admin_profile():
    admin_id = session.get('admin_id')
    print(f"Admin ID from session: {admin_id}")
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401

    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({'error': 'Admin not found'}), 404

    return jsonify({
        'email': admin.email,
        'password': admin.password 
    }), 200

@app.route('/api/admin/update_profile', methods=['PUT'])
def update_admin_profile():
    admin_id = session.get('admin_id')
    print(f"Admin ID from session: {admin_id}")
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    print(f"Data received for update: {data}")
    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({'error': 'Admin not found'}), 404

    admin.email = data.get('email', admin.email)
    admin.password = generate_password_hash(data.get('password', admin.password)) 

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200


@app.route('/api/get_spots/<int:lot_id>/<int:spot_id>', methods=['GET'])
def get_parking_spot(lot_id, spot_id):
    spot = ParkingSpot.query.get(spot_id)

    print(f"Fetching spot with lot_id: {lot_id}, spot_id: {spot_id}")

    if not spot or spot.parking_lot_id != lot_id:
        return jsonify({'error': 'Spot not found'}), 404

    response = {
        'id': spot.parking_spot_id,
        'status': spot.status
    }

    if spot.status == 'O':
        latest_reservation = (
            Reservation.query
            .filter_by(parking_spot_id=spot.parking_spot_id)
            .order_by(Reservation.parking_timestamp.desc())
            .first()
        )

        if latest_reservation:
            user = User.query.get(latest_reservation.user_id)
            response.update({
                'occupiedBy': user.full_name if user else "Unknown",
                'startTime': latest_reservation.parking_timestamp.strftime('%Y-%m-%d %I:%M %p'),
                'expectedEnd': latest_reservation.leaving_timestamp.strftime('%Y-%m-%d %I:%M %p') if latest_reservation.leaving_timestamp else "Not Available"
            })

    return jsonify(response), 200



@app.route('/api/spots/<int:lot_id>/<int:spot_id>', methods=['DELETE'])
def delete_parking_spot(lot_id, spot_id):
    spot = ParkingSpot.query.filter_by(parking_lot_id=lot_id, parking_spot_id=spot_id).first()
    
    if not spot:
        return jsonify({'error': 'Spot not found'}), 404

    if spot.status == 'O':
        return jsonify({'error': 'Cannot delete an occupied spot'}), 400

    parking_lot = ParkingLot.query.get(lot_id)
    if parking_lot:
        parking_lot.number_of_spots = max(parking_lot.number_of_spots - 1, 0)  # Prevent negative count

    db.session.delete(spot)
    db.session.commit()

    return jsonify({'message': 'Spot deleted successfully'}), 200

@app.route('/api/get_spots_occu/<int:lot_id>/<int:spot_id>', methods=['GET'])
def get_occupied_spot(lot_id, spot_id):
    
    reservation = (
        db.session.query(Reservation, ParkingSpot, User)
        .join(ParkingSpot, Reservation.parking_spot_id == ParkingSpot.parking_spot_id)
        .join(User, Reservation.user_id == User.user_id)
        .filter(
            ParkingSpot.parking_lot_id == lot_id,
            ParkingSpot.parking_spot_id == spot_id,
            Reservation.leaving_timestamp.is_(None)  # spot is currently occupied
        )
        .first()
    )

    if not reservation:
        return jsonify({'error': 'No active reservation found for this spot'}), 404

    res, spot, user = reservation

    response_data = {
        'id': res.reservation_id,
        'customer_id': user.user_id,
        'vehicle_number': res.vehicle_number,
        'parking_time': res.parking_timestamp.strftime('%Y-%m-%d %I:%M %p') if res.parking_timestamp else None,
        'estimated_cost': f'₹{calculate_cost(res.parking_timestamp, datetime.utcnow(), spot.parking_lot.price):.2f}',
    }

    return jsonify(response_data), 200


# ======================CUSTOMER ROUTES=======================

@app.route('/api/customer_register', methods=['POST'])
def register_customer():
    data = request.get_json()
    
    required_fields = ['email', 'password', 'full_name', 'address', 'pincode']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data['password'])

    new_customer = User(
        email=data['email'],
        password=hashed_password,
        full_name=data['full_name'],
        address=data['address'],
        pincode=data['pincode'],
        role='user'
    )

    try:
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"message": "Registration successful!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error saving customer details. Please try again."}), 500
    
    
@app.route('/api/parking/history', methods=['GET'])
def get_parking_history():
    id=session.get('customer_id')
    print(f"Customer ID from session: {id}")
    history = Reservation.query.join(ParkingSpot).join(ParkingLot).filter(Reservation.user_id == id).all()

    result = []
    for res in history:
        result.append({
            'parking_lot_id': res.parking_spot.parking_lot_id,
            'parking_spot_id': res.parking_spot_id,
            'address': res.parking_spot.parking_lot.address,
            'vehicle_number': res.vehicle_number,
            'parking_timestamp': res.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'leaving_timestamp': res.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if res.leaving_timestamp else None,
            'status': 'O' if res.leaving_timestamp is None else 'R'
        })

    return jsonify(result)

@app.route('/api/parking/search', methods=['GET'])
def search_parking():
    location = request.args.get('location')
    print(f"Searching for parking in location: {location}")
    print(type(location))
    if location.isnumeric():
        lots = ParkingLot.query.filter(ParkingLot.pincode.ilike(f"%{location}%")).all()
    else:
        lots = ParkingLot.query.filter(ParkingLot.address.ilike(f"%{location}%")).all()

    result = []
    for lot in lots:
        for spot in lot.spots:
            result.append({
                'parking_lot_id': lot.parking_lot_id,
                'parking_spot_id': spot.parking_spot_id,
                'address': lot.address,
                'availability': spot.status
            })
    return jsonify(result)

@app.route('/api/reserve', methods=['POST'])
def reserve_spot():
    data = request.get_json()

    spot_id = data.get('spotId')
    user_email = data.get('userId') 
    vehicle_number = data.get('vehicleNumber')

    
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    
    if not all([spot_id, vehicle_number]):
        return jsonify({"message": "Missing spot ID or vehicle number"}), 400

    
    spot = ParkingSpot.query.get(spot_id)
    if not spot or spot.status != 'A':
        return jsonify({"message": "Parking spot not available"}), 400

    
    reservation = Reservation(
        parking_spot_id=spot_id,
        user_id=user.user_id,
        parking_timestamp=datetime.utcnow(),
        vehicle_number=vehicle_number
    )

    spot.status = 'O'

    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "message": "Reservation successful",
        "reservation_id": reservation.reservation_id
    }), 201

def calculate_cost(start_time, end_time, rate_per_hour):
    duration = end_time - start_time
    duration_hours = duration.total_seconds() / 3600
    # round up to the nearest hour
    duration_hours = int(duration_hours) + (1 if duration_hours % 1 > 0 else 0)
    return round(duration_hours * rate_per_hour, 2)

@app.route('/api/reservation/active', methods=['GET'])
def get_active_reservation():
    lot_id = request.args.get('lotId')
    spot_id = request.args.get('spotId')

    spot = ParkingSpot.query.filter_by(
        parking_lot_id=lot_id,
        parking_spot_id=spot_id,
        status='O'
    ).first()

    if not spot:
        return jsonify({"message": "No active reservation found."}), 404

    reservation = Reservation.query.filter_by(
        parking_spot_id=spot.parking_spot_id,
        leaving_timestamp=None
    ).order_by(Reservation.parking_timestamp.desc()).first()

    if reservation:
        return jsonify({
            "vehicleNumber": reservation.vehicle_number,
            "parkingTime": reservation.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "releasingTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "totalCost": calculate_cost(reservation.parking_timestamp, datetime.utcnow(), spot.parking_lot.price)
        })

    return jsonify({"message": "Active reservation not found"}), 404

@app.route('/api/reservation/release', methods=['POST'])
def release_spot():
    data = request.json
    spot_id = data.get('spotId')

    reservation = Reservation.query.filter_by(
        parking_spot_id=spot_id,
        leaving_timestamp=None
    ).first()

    if not reservation:
        return jsonify({"message": "No active reservation found for this spot."}), 404

    
    now = datetime.utcnow()
    reservation.leaving_timestamp = now

    lot_price = reservation.parking_spot.parking_lot.price
    reservation.parking_cost = calculate_cost(reservation.parking_timestamp, now, lot_price)

    spot = ParkingSpot.query.get(spot_id)
    spot.status = 'A'

    db.session.commit()
    return jsonify({"message": "Spot released", "totalCost": reservation.parking_cost})

@app.route('/api/customer/profile', methods=['GET'])
def get_customer_profile():
    id= session.get('customer_id')
    print(f"Customer ID from session: {id}")
    user = User.query.filter_by(user_id=id, role='user').first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "email": user.email,
        "full_name": user.full_name,
        "address": user.address,
        "pincode": user.pincode
    })

@app.route('/api/customer/update_profile', methods=['PUT'])
def update_customer_profile():
    data = request.json
    email = data.get('email')

    user = User.query.filter_by(email=email, role='user').first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.full_name = data.get('full_name', user.full_name)
    user.address = data.get('address', user.address)
    user.pincode = data.get('pincode', user.pincode)
    if data.get('password'):
        user.password=generate_password_hash(data['password'])
    else:
        user.password = user.password

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})


@app.route('/api/parking-usage-summary', methods=['GET'])
def parking_usage_summary():
    customer_id = session.get('customer_id')

    if not customer_id:
        return jsonify({"error": "Unauthorized access"}), 401

    usage_counts = db.session.query(
        ParkingLot.parking_lot_id,
        ParkingLot.prime_location_name,
        func.count(Reservation.reservation_id).label('usage_count')
    ).join(ParkingSpot, ParkingSpot.parking_lot_id == ParkingLot.parking_lot_id) \
     .join(Reservation, Reservation.parking_spot_id == ParkingSpot.parking_spot_id) \
     .filter(Reservation.user_id == customer_id) \
     .group_by(ParkingLot.parking_lot_id, ParkingLot.prime_location_name) \
     .all()

    result = [
        {
            "lot_name": f"Parking#{i+1}",
            "count": usage.usage_count
        }
        for i, usage in enumerate(usage_counts)
    ]

    return jsonify(result)


# ======================DAILY REMINDER & MONTHLY REPORTS=======================

@app.route('/daily-reminder', methods=['GET'])
def daily_reminder():
    from tasks.reminder import send_daily_reminder
    today = datetime.today().date()
    today_start = datetime.combine(today, datetime.min.time())

    inactive_users = User.query.filter(
        ~User.reservations.any(Reservation.parking_timestamp >= today_start)
    ).all()

    new_lots_today_count = ParkingLot.query.filter(
        ParkingLot.created_at >= today_start
    ).count()

    user_payloads = []
    for user in inactive_users:
        user_payloads.append({
            "full_name": user.full_name,
            "email": user.email,
            "has_visited": False,
            "new_lot_created": new_lots_today_count > 0
        })

    if new_lots_today_count > 0:
        active_users = User.query.filter(
            User.reservations.any(Reservation.parking_timestamp >= today_start)
        ).all()

        for user in active_users:
            user_payloads.append({
                "full_name": user.full_name,
                "email": user.email,
                "has_visited": True,
                "new_lot_created": True
            })

    task = send_daily_reminder.delay(user_payloads)
    return f"✅ Reminder task triggered! Task ID: {task.id} | Users to notify: {len(user_payloads)}"


@app.route('/monthly-report', methods=['GET'])
def monthly_report():
    from tasks.monthly_report import send_monthly_activity_reports
    print("📊 Generating monthly reports...")

    # for last month
    today = datetime.today()
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_last_month = today.replace(day=1) - timedelta(days=1)

    # for this month
    # today = datetime.today()
    # first_day_this_month = today.replace(day=1)
    # last_day_this_month = today


    users = User.query.all()
    reports = []

    for user in users:
        reservations = Reservation.query.filter(
            Reservation.user_id == user.user_id,
            Reservation.parking_timestamp >= first_day_last_month,
            Reservation.parking_timestamp <= last_day_last_month
        ).all()

        if not reservations:
            continue

        total_bookings = len(reservations)
        total_cost = sum(r.parking_cost or 0 for r in reservations)

        lot_counts = {}
        for r in reservations:
            lot = r.parking_spot.parking_lot
            lot_name = lot.prime_location_name
            lot_counts[lot_name] = lot_counts.get(lot_name, 0) + 1

        most_used_lot = max(lot_counts, key=lot_counts.get)
        

        reports.append({
            "full_name": user.full_name,
            "email": user.email,
            "total_bookings": total_bookings,
            "total_cost": total_cost,
            "most_used_lot": most_used_lot
        })
        # print(reports)

    task = send_monthly_activity_reports.delay(reports)
    return f"📬 Monthly report task triggered! Task ID: {task.id} | Users: {len(reports)}"


# ======================CSV EXPORT ROUTES=======================


@app.route('/api/trigger-export', methods=['POST'])
def trigger_export():
    from tasks.export_csv import export_parking_history_to_csv
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    reservations = Reservation.query.filter_by(user_id=user.user_id).all()
    if not reservations:
        return jsonify({"message": "No reservations found"}), 204

    data = []
    for r in reservations:
        data.append({
            "slot_id": r.parking_spot_id,
            "spot_id": r.parking_spot.parking_spot_id,
            "lot_id": r.parking_spot.parking_lot_id,
            "location": r.parking_spot.parking_lot.address,
            "vehicle_number": r.vehicle_number,
            "cost": r.parking_cost or 0,
            "start_time": r.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": r.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.leaving_timestamp else "Still Parked"
        })

    task = export_parking_history_to_csv.delay(email, data)

    return jsonify({
        "message": "📦 Export task triggered successfully!",
        "task_id": task.id,
        "records": len(data)
    })

@app.route('/download/<filename>')
def download_file(filename):
    from flask import send_from_directory
    import os

    # absolute path
    export_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "exports"))
    file_path = os.path.join(export_dir, filename)
    print(f"[DOWNLOAD ROUTE] Looking for file: {file_path}")

    return send_from_directory(export_dir, filename, as_attachment=True)


@app.route('/api/export-status/<task_id>', methods=['GET'])
def export_status(task_id):
    result = AsyncResult(task_id, app=celery)
    if result.state == 'SUCCESS':
        filename = result.result
        print(f"Export completed successfully: {filename}")
        download_url = request.host_url.rstrip("/") + f"/download/{filename}"
        print(f"Download URL: {download_url}")
        return jsonify({
            "status": "ready",
            "downloadUrl": download_url
        })
    elif result.state in ['PENDING', 'STARTED']:
        return jsonify({"status": "processing"})
    else:
        return jsonify({"status": "failed"})


# ======================SCHEDULER SETUP=======================

def schedule_reminder():
    with app.app_context():
        print("⏰ Triggering daily reminder job...")
        requests.get("http://127.0.0.1:5000/daily-reminder")

def schdule_monthly_report():
    with app.app_context():
        print("📅 Triggering monthly report job...")
        requests.get("http://127.0.0.1:5000/monthly-report")

def export_csv():
    with app.app_context():
        print("📦 Triggering CSV export job...")
        requests.get("http://127.0.0.1:5000/trigger-export")

scheduler = BackgroundScheduler()
scheduler.add_job(schedule_reminder, 'cron', hour=17, minute=30)
scheduler.add_job(schdule_monthly_report, 'cron',day=1,hour=12, minute=30)
scheduler.start()


if __name__ == '__main__':
    app.run(debug=True)