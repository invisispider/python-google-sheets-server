from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import pygsheets

# if modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def main():
        creds = None
        # DEVELOPMENT ONLY:
        if os.path.exists('./token.json'):
                        creds = Credentials.from_authorized_user_file('./token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        './client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('./token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

# DEV ONLY 
client = pygsheets.authorize(client_secret='./client_secret.json')

# client = pygsheets.authorize(client_secret='../client_secret.json')

# redir_uris = r'http://127.0.0.1:5000/oauth2callback'
# flow.redirect_uri = redir_uris

# Generate URL for request to Google's OAuth 2.0 server.
# Use kwargs to set optional request parameters.

# authorization_url, state = flow.authorization_url(
#     # Enable offline access so that you can refresh an access token without
#     # re-prompting the user for permission. Recommended for web server apps.
#     access_type='offline',
#     #UPDATE WITH EMAIL ADDRESS
#     login_hint='<MY_EMAIL_ADDRESS>',
#     # Enable incremental authorization. Recommended as a best practice.
#     include_granted_scopes=True)

if __name__ == '__main__':
    main()
