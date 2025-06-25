from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
# Initializing the database
db = SQLAlchemy()

# -------------------------------
# User Model
# -------------------------------
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password =   db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(10), default='user')  

    reservations = db.relationship(
        'Reservation',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

# -------------------------------
# Admin Model 
# -------------------------------
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default='admin')

# -------------------------------
# Parking Lot Model
# -------------------------------
class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'
    parking_lot_id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    spots = db.relationship(
        'ParkingSpot',
        backref='parking_lot',
        lazy=True,
        cascade='all, delete-orphan'
    )

# -------------------------------
# Parking Spot Model
# -------------------------------
class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'
    parking_spot_id = db.Column(db.Integer, primary_key=True)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.parking_lot_id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(1), default='A')  # A - Available, O - Occupied

    reservations = db.relationship(
        'Reservation',
        backref='parking_spot',
        lazy=True,
        cascade='all, delete-orphan'
    )

# -------------------------------
# Reservation Model
# -------------------------------
class Reservation(db.Model):
    __tablename__ = 'reservation'
    reservation_id = db.Column(db.Integer, primary_key=True)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.parking_spot_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
    vehicle_number = db.Column(db.String(20), nullable=True)