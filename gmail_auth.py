import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    credentials = None

    # Check if credentials.json is provided through environment variable
    creds_json = os.getenv('GOOGLE_CREDENTIALS')
    if creds_json:
        credentials_data = json.loads(creds_json)
        with open('credentials.json', 'w') as file:
            json.dump(credentials_data, file)

        # Use InstalledAppFlow for device authorization (console mode)
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        credentials = flow.run_console()  # Use console flow instead of local server

    # If credentials exist, check if they're valid or need refresh
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    else:
        raise Exception("No credentials provided")

    return credentials

