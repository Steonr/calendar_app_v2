from infra.gmail_service import GmailApi
from infra.PubSub_API.subscriber import SubscriberClient
from infra.authorization import AuthorizationService

import logging

from googleapiclient.errors import HttpError

def main():

    file_path = "./src/auth/gmail/token.pickle"
    secret_file = "./src/auth/gmail/client_secretfile.json"
    
    auth = AuthorizationService(file_path, secret_file)
    creds = auth.get_credentials()
    gmail = GmailApi(SubscriberClient, creds)
    sub = SubscriberClient()
    
    sub.streaming_pull()
    
    # try:
    #     response = gmail.request()
    #     print(f"response: {response}")
    # except HttpError as error:
    #     print(f"Error: {error}")


if __name__ == "__main__":
    main()