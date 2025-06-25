from celery_worker import celery
from datetime import datetime
from email.mime.text import MIMEText
import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import os

# === CONFIGURATION ===
TOKEN_PATH = os.path.abspath('token.json')
print(f"Using token file: {TOKEN_PATH}")
SENDER_EMAIL = "raghvigupta2005@gmail.com"  

# === UTILITY FUNCTIONS ===

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}

def send_email_via_gmail(subject, body, to_email):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/gmail.send'])
    service = build('gmail', 'v1', credentials=creds)
    message = create_message(SENDER_EMAIL, to_email, subject, body)
    sent = service.users().messages().send(userId='me', body=message).execute()
    print(f"✅ Email sent to {to_email}: Message ID {sent['id']}")
    return sent

# === CELERY TASK ===

@celery.task(name='tasks.reminder.send_daily_reminder')
def send_daily_reminder(users):
    """
    users: List of dictionaries, each with:
        {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'has_visited': False,
            'new_lot_created': True
        }
    """
    print(f"[{datetime.now()}] ✅ Starting Gmail daily reminders for {len(users)} users")

    subject = "🚗 Friendly Parking Reminder"

    for user in users:
        name = user.get("full_name", "there").split()[0] 
        email = user.get("email")
        has_visited = user.get("has_visited", True)
        new_lot = user.get("new_lot_created", False)

        if has_visited and not new_lot:
            continue

        message_lines = [f"Hey {name}, Hope you're doing well!"]

        if not has_visited:
            message_lines.append("We noticed you haven’t parked today.")

        if new_lot:
            message_lines.append("We are proud to announce that a new parking lot has been added recently.")

        message_lines.append("Book your spot now if you need one! 🚘")
        message_lines.append("Hurry up, spots are filling fast! 🏃‍♂️")

        body = "\n".join(message_lines)

        try:
            send_email_via_gmail(subject, body, email)
        except Exception as e:
            print(f"❌ Failed to send to {email}: {e}")

    return "📬 Daily personalized reminder emails sent"
