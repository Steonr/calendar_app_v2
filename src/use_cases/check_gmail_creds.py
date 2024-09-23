from infra.gmail_service import GmailService

class CheckGmailCreds:
    def __init__(self, gmail_service: GmailService):
        self.gmail_service = gmail_service

    def execute(self) -> bool:
        return self.gmail_service.check_creds()
