from celery_worker import celery
from datetime import datetime
from email.mime.text import MIMEText
import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# === CONFIGURATION ===
TOKEN_PATH = os.path.abspath('token.json')
print(f"Using token file: {TOKEN_PATH}")
SENDER_EMAIL = "raghvigupta2005@gmail.com" 

# === UTILITY FUNCTIONS ===

def create_message(sender, to, subject, message_html):
    message = MIMEMultipart("alternative")
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    # HTML part
    html_part = MIMEText(message_html, "html")
    message.attach(html_part)

    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {"raw": raw.decode()}

def send_email_via_gmail(subject, body, to_email):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/gmail.send'])
    service = build('gmail', 'v1', credentials=creds)
    message = create_message(SENDER_EMAIL, to_email, subject, body)
    sent = service.users().messages().send(userId='me', body=message).execute()
    print(f"✅ Email sent to {to_email}: Message ID {sent['id']}")
    return sent

# === CELERY TASK ===

@celery.task(name='tasks.monthly_report.send_monthly_activity_reports')
def send_monthly_activity_reports(reports):
    print(f"[{datetime.now()}] Sending monthly reports to {len(reports)} users...")

    for report in reports:
        name = report["full_name"].split()[0]
        email = report["email"]
        total = report["total_bookings"]
        cost = report["total_cost"]
        lot = report["most_used_lot"]

        html = f"""
        <html>
        <body style="margin: 0; padding: 0; background-color: #e3eafc;">
            <div style="max-width: 600px; margin: 30px auto; background: #ffffff; border-radius: 10px; box-shadow: 0 0 12px rgba(0, 0, 0, 0.1); overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                
                <!-- Header -->
                <div style="background: linear-gradient(90deg, #1a237e, #3f51b5); color: white; padding: 20px 30px;">
                    <h2 style="margin: 0; font-size: 24px;">📊 Monthly Parking Report</h2>
                </div>

                <!-- Content -->
                <div style="padding: 30px; color: #2c3e50;">
                    <p style="font-size: 16px;">Hi <strong>{name}</strong>,</p>
                    <p style="font-size: 15px;">Here's your personalized parking summary for <strong>last month</strong>:</p>

                    <ul style="font-size: 15px; line-height: 1.8; padding-left: 20px;">
                        <li><strong>Total Bookings:</strong> {total}</li>
                        <li><strong>Total Amount Spent:</strong> ₹{cost:.2f}</li>
                        <li><strong>Most Visited Parking Lot:</strong> {lot}</li>
                    </ul>

                    <p style="margin-top: 30px; font-size: 15px;">Thanks for staying with <strong>ParkEase</strong> 🚗. We hope to see you parking again soon!</p>
                </div>

                <!-- Footer -->
                <div style="background-color: #dfe3ee; text-align: center; padding: 12px; font-size: 13px; color: #555;">
                    &copy; {datetime.now().year} <strong>ParkEase</strong> · All rights reserved.
                </div>
            </div>
        </body>
        </html>
        """



        try:
            send_email_via_gmail("📅 Your Monthly Parking Report", html, email)
        except Exception as e:
            print(f"❌ Failed to send to {email}: {e}")

    return "✅ All reports sent"
