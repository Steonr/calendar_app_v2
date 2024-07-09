import logging
from frameworks_drivers.logging_setup import setup_logging

class LoggingService:
    def __init__(self):
        setup_logging()
        self.logger = logging.getLogger("main")

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)