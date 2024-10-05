# fetch_newsletters.py

from gmail_auth import authenticate_gmail
import base64
from email import message_from_bytes
from email.policy import default

# Define the email addresses of the newsletters
NEWSLETTER_SENDERS = [
    "newsletter@thedailyrip.stocktwits.com",
    "dan@tldrnewsletter.com",
    "googledev-noreply@google.com"
]

def fetch_newsletters():
    service = authenticate_gmail()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=50).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No new messages found.')
        return []

    newsletters = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
        raw_email = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
        email_message = message_from_bytes(raw_email, policy=default)
        from_email = email_message['From']

        if from_email and any(sender in from_email for sender in NEWSLETTER_SENDERS):
            # Get the plain text part of the email
            text_content = ''
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == 'text/plain':
                        text_content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
            else:
                text_content = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')

            if text_content:
                newsletters.append(text_content)

    return newsletters
