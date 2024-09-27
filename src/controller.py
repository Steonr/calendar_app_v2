from infra.gmail_service import GmailApi
from infra.PubSub_API.subscriber import SubscriberClient
from infra.PubSub_API.publisher import PublisherClient
from infra.authorization import AuthorizationService
from infra.response_model import ResponsModel

import os
import logging
import time

from googleapiclient.errors import HttpError

def main():

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './src/auth/google_api/application_default_credentials.json'
    file_path = "./src/auth/gmail/token.pickle"
    secret_file = "./src/auth/gmail/client_secretfile.json"
    response_path = './src/data/response/response.json'
    messages_path = './src/data/response/messages.json'
    
    auth = AuthorizationService(file_path, secret_file)
    creds = auth.get_credentials()
    gmail = GmailApi(SubscriberClient, creds)
    sub = SubscriberClient()
    pub = PublisherClient()
    

    try:
        data = gmail.watch_request()
        response = ResponsModel.from_dict(data)
        response.save_data(response_path)
        print(f"History ID: {response.historyId}")
        print(f"expiration: {response.expiration}")
    except HttpError as error:
        print(f"Error: {error}")

    while True:
        sub.pull_message()


if __name__ == "__main__":
    main()