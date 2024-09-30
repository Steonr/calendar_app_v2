from infra.gmail_service import GmailApi
from infra.PubSub_API.subscriber import SubscriberClient
from infra.PubSub_API.publisher import PublisherClient
from infra.authorization import AuthorizationService
from infra.response_model import ResponsModel, HistoryList, Message

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
    message_path = './src/data/response/last_message.json'
    history_list_path = './src/data/response/history_list.json'
    
    auth = AuthorizationService(file_path, secret_file)
    creds = auth.get_credentials()
    gmail = GmailApi(SubscriberClient, creds)
    sub = SubscriberClient()
    pub = PublisherClient()
    history_list = HistoryList()
    mail = Message()
    
    

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
        if response:= sub._message:
            history_list.data = gmail.get_messages()
            history_list.save_data(history_list_path)
            history_list.get_last_message()
            mail.data = gmail.get_message(history_list.last_message)
            print("Title: ", mail.get_title)
            mail.save_data(message_path)

if __name__ == "__main__":
    main()