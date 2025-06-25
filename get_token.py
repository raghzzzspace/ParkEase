import os
import pickle
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# SCOPES: We only need to send email
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the token
    with open('token.json', 'w') as token_file:
        token_file.write(creds.to_json())

    print("✅ token.json created!")

if __name__ == '__main__':
    main()
