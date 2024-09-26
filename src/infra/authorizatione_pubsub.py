import os
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class AuthorizationPubSubService:
    def __init__(self, token_path: str, secret_file_path: str):
        """Initialize the Pub Sub API with specified token and secret file paths.

        Args:
            token_path (str): The file path to the token file used for authentication.
            secret_file_path (str): The file path to the secret file containing API credentials.

        Returns:
            None
        """
        self._creds = None
        self._scopes = ['https://www.googleapis.com/auth/gmail.readonly']
        self._token_path = token_path
        self._secret_file_path = secret_file_path

    def get_credentials(self) -> None:
        pass

    def _refresh_or_validate_credentials(self) -> None:
        pass

    def _validate_credentials(self) -> Credentials:
        pass
        
    def save_credentials(self) -> None:
        pass