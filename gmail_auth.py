import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Get the credentials and token JSON from environment variables
CREDENTIALS_JSON = os.environ.get("CREDENTIALS_JSON")
TOKEN_JSON = os.environ.get("TOKEN_JSON")

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    if not CREDENTIALS_JSON:
        raise Exception("No credentials provided")

    creds = None
    
    # If token.json is in the environment, load it
    if TOKEN_JSON:
        token = json.loads(TOKEN_JSON)
        creds = Credentials.from_authorized_user_info(token, SCOPES)
    
    # If no (valid) token available, let the user log in and generate a new one
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_info = json.loads(CREDENTIALS_JSON)
            flow = InstalledAppFlow.from_client_config(creds_info, SCOPES)
            creds = flow.run_local_server(port=0)

        # If new credentials were created, save them in the environment
        token_data = creds.to_json()
        # You can optionally add code to store token_data back to Azure env variables if needed.

    return creds

