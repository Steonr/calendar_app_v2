from domain.entities.gmail import Request, Response
from infra.gmail_repository import GmailRepository
from infra.config_loader import ConfigLoader
from infra.authorization import AuthorizationService
from infra.PubSub_API.subscriber import SubscriberClient
from infra.ultility import get_json, save_json
import logging

from googleapiclient.errors import HttpError

class GmailController:

    def __init__(self):
        self.config_loader = ConfigLoader('./config.json')
        self.data_paths = self.config_loader.get_data_paths()
        self.request = self.config_loader.get_request()
        self.auth = AuthorizationService(self.data_paths['token'], self.data_paths['client_secretfile'])
        self.creds = self.auth.get_credentials()
        self.sub = SubscriberClient()

    def start(self):
        Request.request = self.request
        gmail = GmailRepository(SubscriberClient, self.creds)
        response = Response.get_data(self.data_paths['response'])
        if not response.historyId: 
            response_data = gmail.watch_request(Request.request)
            response = response.from_dict(response_data)
            response.save(self.data_paths['response'])


        while True:    
            gmail.get_history_list(response.historyId)
            self.sub.pull_message()
        