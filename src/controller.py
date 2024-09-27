from infra.gmail_service import GmailApi
from infra.PubSub_API.subscriber import SubscriberClient
from infra.PubSub_API.publisher import PublisherClient
from infra.authorization import AuthorizationService

import os
import logging

from googleapiclient.errors import HttpError

def main():

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './src/auth/google_api/application_default_credentials.json'
    file_path = "./src/auth/gmail/token.pickle"
    secret_file = "./src/auth/gmail/client_secretfile.json"
    
    auth = AuthorizationService(file_path, secret_file)
    creds = auth.get_credentials()
    gmail = GmailApi(SubscriberClient, creds)
    sub = SubscriberClient()
    pub = PublisherClient()

    creds = auth._creds
    # pub.streaming_push()
    # sub.streaming_pull()

    try:
        response = gmail.request()
        print(f"response: {response}")
    except HttpError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()