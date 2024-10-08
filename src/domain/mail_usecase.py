from domain.entities.gmail import Request, Response
from infra.config_loader import ConfigLoader
from infra.PubSub_API.subscriber import SubscriberClient
from infra.interfaces.interface_gmail import IGmailRepository
from infra.interfaces.interface_subscriber import ISubscriber
from infra.config_loader import ConfigLoader


class WatchRequestUseCase():
    def __init__(self, request_dict, IGmailRepository):
        self.response = Response("", "")
        self.request_dict = request_dict
        self.config_loader = ConfigLoader('./config.json')
        self.data_paths = self.config_loader.get_data_paths()
        self.request = self.config_loader.get_request()
        self.sub = SubscriberClient()
        self.gmail = IGmailRepository
    def watch_request(self):
        self.response = self.gmail.watch_request(self.request_dict)
        self.response.save(self.data_paths['response'])
        return self.response
    def stop_request(self):
        self.gmail.stop_request()

    def watch_expired(self):
        ''' Check for response file and check if it contains a historyId
            and the status of the expiration
        '''
        self.response = self.response.get_data(self.data_paths['response'])
        if self.response.historyId:
            print("Watch request still valid with:")
            print(f"HistoryId: {self.response.historyId} ")
            print(f"Expiration: {self.response.expiration}")
        return not self.response.historyId

    def execute(self):
        if self.watch_expired():
            self.stop_request()
            self.watch_request()
        return self.response

class ListenForMessageUseCase: 
    def __init__(self, ISubscriber, IGmailRepository):
        self.sub = ISubscriber
        self.gmail = IGmailRepository
        self.config = ConfigLoader('./config.json')
        self.data_paths = self.config.get_data_paths()
        self.message = self.config.get_message()
    def listen(self, message_requirements, response_path, response) -> str:
        old_historyId = response.historyId
        message_id = ""
        while True:
            response.historyId = self.sub.pull_message()
            if response.historyId not in [old_historyId, '']:
                response.save(response_path)
                print(f"New historyId: {response.historyId}")
                self.gmail.get_history_list(self.data_paths['history_list'], old_historyId)
                self.gmail.get_subjects_from_history_list()
                message_id = self.gmail.search_history_list_subject(self.message['subject'])
                if message_id != "":
                    return message_id
                old_historyId = response.historyId

class AttachmentUseCase: 
    def __init__(self, IGmailRepository):
        self.gmail = IGmailRepository
    def get_attachment(self, path, message_id):
        attachment_id = self.gmail.get_attachment_ids(message_id)
        self.gmail.get_attachment(path, message_id, attachment_id)
        attachment_name = self.gmail.get_attachment_name(message_id, attachment_id)
        print(f"\nAttachment: {attachment_name}\nAttachment id: {attachment_id} saved to:\n{path}")