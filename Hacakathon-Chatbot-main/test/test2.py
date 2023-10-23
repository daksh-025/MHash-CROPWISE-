from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json


# Load credentials from JSON file
with open('token.json') as json_file:
    credentials = json.load(json_file)

oauth_credentials = Credentials.from_authorized_user_info(credentials)

service = build('gmail', 'v1', credentials=oauth_credentials)

# Call the Gmail API to list labels
results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

if not labels:
    print('No labels found.')
else:
    print('Labels:')
    for label in labels:
        print(label['name'])

# Load credentials and create Gmail API service
# ...
# Refer to the previous steps for loading credentials and building the service

# Compose the email details
recipient_email = 'recipient@example.com'
subject = 'Hello from Gmail API'
message_text = 'This is the email body.'

# Create the Message object
message = MIMEText(message_text)
message['to'] = recipient_email
message['subject'] = subject
raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
send_request = service.users().messages().send(userId='me', body={'raw': raw_message})
response = send_request.execute()

print('Email sent successfully.')
