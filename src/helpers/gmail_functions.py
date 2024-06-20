import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import logging
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from helpers.helpers import give_dir
from config import SECRET_FILE_PATH, TOKEN_PATH

logger = logging.getLogger("gmail")

def create_creds(client_secretFile):
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    flow = InstalledAppFlow.from_client_secrets_file(client_secretFile, SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    path_token = give_dir(__file__, 2) + "/src/auth/Gmail/token.pickle"
    with open(path_token, 'wb') as token:
        pickle.dump(creds, token)
    return creds

def get_creds(path_token):
    logger.info("checking for token")
    creds = None
    if os.path.exists(path_token):
        with open(path_token, 'rb') as token:
            creds = pickle.load(token)
            logger.info("Token present and loaded")
    else:
        logger.info(f"No token available at path: {path_token}")
    return creds

def check_creds():

    creds = get_creds(TOKEN_PATH)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = create_creds(SECRET_FILE_PATH)
    return creds