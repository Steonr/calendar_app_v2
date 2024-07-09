import logging
from config import LOG_FILE_PATH

def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8',
        level=logging.DEBUG,
        handlers=[logging.FileHandler(LOG_FILE_PATH), logging.StreamHandler()])