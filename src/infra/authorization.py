import os
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class AuthorizationService:
    def __init__(self, token_path: str, secret_file_path: str):
        """Initialize the Gmail service with specified token and secret file paths.

        Args:
            token_path (str): The file path to the token file used for authentication.
            secret_file_path (str): The file path to the secret file containing API credentials.

        Returns:
            None
        """
        self._creds = None
        self._scopes = ['https://www.googleapis.com/auth/gmail.readonly',  
                        "https://www.googleapis.com/auth/gmail.modify",  
                        'https://mail.google.com/']
        self._token_path = token_path
        self._secret_file_path = secret_file_path

    def get_credentials(self) -> None:
        """Retrieve user credentials from a specified token file.
        """
        if os.path.exists(self._token_path):
            with open(self._token_path, 'rb') as token:
                self._creds = pickle.load(token)
                
        if not self._creds or not self._creds.valid:
            self._refresh_or_validate_credentials()
            self.save_credentials()
        return self._creds

    def _refresh_or_validate_credentials(self) -> None:
        if self._creds and self._creds.expired and self._creds.refresh_token:
            self._creds.refresh(Request())   
        else:
            self._creds = self._validate_credentials()

    def _validate_credentials(self) -> Credentials:
        flow = InstalledAppFlow.from_client_secrets_file(
            self._secret_file_path, self._scopes
        )
        return flow.run_local_server(port=0)
        
    def save_credentials(self) -> None:
        # Save the credentials for the next run
        with open(self._token_path, "wb") as token:
            pickle.dump(self._creds, token)