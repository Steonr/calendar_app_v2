import logging
from interface_adapters.logging_service import LoggingService
from frameworks_drivers.gmail_api import GmailAPI
from interface_adapters.gmail_service import GmailService
from use_cases.check_gmail_creds import CheckGmailCreds

def main():
    logger_service = LoggingService()
    logger_service.info("Application started")

    gmail_api = GmailAPI()
    gmail_service = GmailService(gmail_api)
    check_gmail_creds_use_case = CheckGmailCreds(gmail_service)

    try:
        if not check_gmail_creds_use_case.execute():
            logger_service.error("Gmail credentials check failed")
            return
        logger_service.info("Gmail credentials verified successfully")
        # TODO: Add functionality to read email and process attachments
    except Exception as e:
        logger_service.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()