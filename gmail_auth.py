import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    credentials = None

    # Check for credentials.json from environment
    creds_json = os.getenv('GOOGLE_CREDENTIALS')
    if creds_json:
        credentials_data = json.loads(creds_json)
        with open('credentials.json', 'w') as file:
            json.dump(credentials_data, file)

        # Use InstalledAppFlow with local server method for Azure
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        credentials = flow.run_local_server(port=0)  # Use local server for OAuth

    else:
        raise Exception("No credentials provided")

    return credentials


