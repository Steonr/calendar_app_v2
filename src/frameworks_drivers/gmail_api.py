import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config import SECRET_FILE_PATH, TOKEN_PATH
from src.helpers.helpers import give_dir

class GmailAPI:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def create_creds(self):
        flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE_PATH, self.SCOPES)
        creds = flow.run_local_server(port=0)
        path_token = give_dir(__file__, 2) + "/auth/Gmail/token.pickle"
        with open(path_token, 'wb') as token:
            pickle.dump(creds, token)
        return creds

    def get_creds(self):
        creds = None
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        return creds
