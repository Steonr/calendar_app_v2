from domain.entities.gmail import Request, Response

from abc import ABC, abstractmethod
class IGmailRepository(ABC):
    def __init__(self, SubscriberClient, credentials):
        self.history_list
        self._subject
    def _save_history_list(self, JSON_path) -> None:
        ''' save history list in JSON-file'''
    def watch_request(self, request: dict) -> Response:
        pass
    def stop_request(self) -> None:
        pass
    def get_label_list(self):
        pass
    def get_message(self, Id: str) -> Response:
        pass
    def get_messages(self) -> Response:
        pass
    def get_subject(self):
        pass
    def get_history_list(self, Id: str) -> None:
        ''' get history list from start of the historyId'''
    def search_history_list_subject(self) -> None:
        pass
    def get_attachment_ids(self, message_id):
        pass
    def get_attachment(self, attachment_id):
        pass
    def get_attachment_name(self, message_id, attachment_id):
        pass
    def get_subjects_from_history_list(self):
        pass