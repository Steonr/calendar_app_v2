import sys
import os
abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)
dir_up = os.path.dirname(dir_name)
base_dir = os.path.dirname(dir_up)
sys.path.append(base_dir)
import logging
from functools import reduce
from config import LOG_FILE_PATH

def give_dir(current_file, level_up = 0):
    dir = os.path.dirname(current_file)
    # if level > 0, then iterate so that you can go up in folder hierarchy
    dir = reduce(lambda d, _: give_dir(d), range(level_up), dir)
    return dir

def setup_logging():
    logger_path = LOG_FILE_PATH
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
                        datefmt='%Y-%m-%d %H:%M:%S',
                        encoding='utf-8', 
                        level=logging.DEBUG, 
                        handlers=[logging.FileHandler(logger_path), logging.StreamHandler()]
                    )

if __name__ == "__main__":
    pass