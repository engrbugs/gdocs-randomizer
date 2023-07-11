from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
###########################################################
SCOPES = ['https://www.googleapis.com/auth/documents']
DOCUMENT_ID = '1-vH-4M19e_X4ArdJ5UzZXgGDLIyEosEuM7WiWdAnQ3s'
###########################################################

def logIn():
    """Logs in and returns the credentials."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('secret/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def readTitle(creds):
    """Reads and prints the title of the document."""
    try:
        service = build('docs', 'v1', credentials=creds)
        document = service.documents().get(documentId=DOCUMENT_ID).execute()
        print('The title of the document is: {}'.format(document.get('title')))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    creds = logIn()
    readTitle(creds)
