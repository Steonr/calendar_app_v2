from domain.entities.gmail import Request, Response
from infra.gmail_repository import GmailRepository
from infra.config_loader import ConfigLoader
from infra.authorization import AuthorizationService
from infra.PubSub_API.subscriber import SubscriberClient
from infra.ultility import get_json, save_json
from use_cases.mail_usecase import WatchRequestUseCase, ListenForMessageUseCase
from use_cases.excel_usecase import ExcelUseCase

import logging
import os

from googleapiclient.errors import HttpError

class GmailController:
    def __init__(self):
        self.config_loader = ConfigLoader('./config.json')
        self.data_paths = self.config_loader.get_data_paths()
        self.message_req = self.config_loader.get_message()
        self.request = self.config_loader.get_request()
        self.creds = self._authorize()
        self.sub = SubscriberClient()
        self._set_environment_vars()

    def _set_environment_vars(self):
         os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.data_paths['google_api_creds']
    def _authorize(self):
        ''' Authorize and get credentials
        '''
        token = self.data_paths['token']
        client_secret_file = self.data_paths['client_secretfile']
        auth = AuthorizationService(token, client_secret_file)
        return auth.get_credentials()
    def start(self):
        response_path = self.data_paths['response']
        get_message = self.message_req
        history_list_path = self.data_paths['history_list']
        attachment_path = self.data_paths['attachment']

        gmail = GmailRepository(self.creds)
        watch_request_usecase = WatchRequestUseCase(self.request, gmail)
        message_usecase = ListenForMessageUseCase(self.sub, gmail)
        excel_usecase = ExcelUseCase()
        
        response = watch_request_usecase.execute()
        while True: 
            message_usecase.listen(history_list_path, response_path, response)
            message_usecase.get_attachment(attachment_path)
            excel_usecase.read_excel()
                