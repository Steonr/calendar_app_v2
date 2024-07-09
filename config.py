import os
import sys
abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)
sys.path.append(dir_name)

BASE_DIR = dir_name
# TOKEN_PATH = os.path.join(BASE_DIR, 'src/auth/Gmail/token.pickle')
# SECRET_FILE_PATH = os.path.join(BASE_DIR, 'src/auth/Gmail/client_secretfile.json')
# LOG_FILE_PATH = os.path.join(BASE_DIR, 'logs/app.log')


SECRET_FILE_PATH = 'path_to_secret_file.json'
TOKEN_PATH = 'path_to_token.pickle'
LOG_FILE_PATH = 'application.log'