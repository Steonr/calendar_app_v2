from infra.authorization import AuthorizationService
import logging

def main():

    file_path = "./src/auth/gmail/token.pickle"
    secret_file = "./src/auth/gmail/client_secretfile.json"
    
    auth = AuthorizationService(file_path, secret_file)
    auth.get_credentials()

if __name__ == "__main__":
    main()