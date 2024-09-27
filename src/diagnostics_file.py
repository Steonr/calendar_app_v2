import json
import pickle

file_path = "./src/auth/gmail/token.pickle"
secret_file = "./src/auth/gmail/client_secretfile.json"

# Load token.json
with open(file_path, 'rb') as f:
    obj = pickle.load(f)

token = obj.__dict__

# token = json.dumps(token)

print(token)
