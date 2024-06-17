import logging
from src.lib.helpers import setup_logging, give_dir
from src.lib.gmail_functions import check_creds

def main():
    # Testing git push
    try:
        setup_logging()
        logger = logging.getLogger("main")
        logger.info("Application started")


        # Check Gmail credentials
        if not check_creds():
            logger.error("Gmail credentials check failed")
            return

        logger.info("Gmail credentials verified successfully")
        
        # TODO: Add functionality to read email and process attachments
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
