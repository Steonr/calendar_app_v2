import logging
from frameworks_drivers.gmail_api import GmailAPI

class GmailService:
    def __init__(self, gmail_api: GmailAPI):
        self.gmail_api = gmail_api

    def check_creds(self) -> bool:
        creds = self.gmail_api.get_creds()
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                creds = self.gmail_api.create_creds()
        return creds is not None    