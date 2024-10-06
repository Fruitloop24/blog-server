import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build  # Import to create service object

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    credentials = None
    CREDENTIALS_PATH = 'credentials.json'
    TOKEN_PATH = 'token.json'

    # Check if token.json exists (previously authenticated session)
    if os.path.exists(TOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # If no valid credentials, do the OAuth flow
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())  # Refresh the token if it's expired
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            credentials = flow.run_local_server(port=0)  # OAuth flow

        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(credentials.to_json())

    # Build the Gmail service object
    service = build('gmail', 'v1', credentials=credentials)

    return service  # Return Gmail API service object






