# gmail_auth.py

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define paths and constants
TOKEN_PATH = 'token.json'          # Path to save the user's access and refresh tokens
CREDENTIALS_PATH = 'credentials.json'  # Path to your client credentials JSON file
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None

    # Check if token.json exists; if so, use the stored credentials
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # If there are no valid credentials, initiate the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the credentials
            creds.refresh(Request())
        else:
            # Run the OAuth flow to get new credentials
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())

    # Build the Gmail API service object
    service = build('gmail', 'v1', credentials=creds)
    return service

