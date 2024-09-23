import logging
from frameworks_drivers.gmail_api import GmailAPI

import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class Authorization:
    def __init__(self):
        self.creds = None
        self._scopes = ['https://www.googleapis.com/auth/gmail.readonly']
        self._token_path = "/auth/gmail/token.pickle"
        self._secret_file_path = "/auth/google_calendar/client_secretfile.json"
        self.__authorize__()

    def __authorize__(self):
        creds = self.get_credentials()
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
            creds = self.validate_credentials(creds)
            self.save_credentials()

    def get_credentials(self) -> None:
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self._token_path):
            self.creds = Credentials.from_authorized_user_file(self._token_path, self._secret_file_path)

    def validate_credentials(self) -> Credentials:
        flow = InstalledAppFlow.from_client_secrets_file(
            self._secret_file_path, self._scopes
        )
        return flow.run_local_server(port=0)
        
    def save_credentials(self) -> None:
        # Save the credentials for the next run
        with open(self._token_path, "w") as token:
            token.write(self.creds.to_json())
