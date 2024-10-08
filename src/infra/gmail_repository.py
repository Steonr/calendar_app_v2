from infra.interfaces.interface_gmail import IGmailRepository
from domain.entities.gmail import Response
from infra.ultility import save_json

import base64

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

class GmailRepository(IGmailRepository):
    def __init__(self, credentials):
        self._service = build("gmail", "v1", credentials=credentials)
        self._service_account = 'gmail-api-push@system.gserviceaccount.com'
        self.historylist = None
        self._subject = None
        self._history_id_list = []
        self._history_message_list = []
    def _save_history_list(self, path):
        save_json(self.historylist, path)
    def watch_request(self, request_dict):
        response_dict = self._service.users().watch(userId='me', body=request_dict).execute()
        print(f"Watch request succesful with historyId: {response_dict['historyId']}")
        response = Response("","")
        return response.from_dict(response_dict)
    def stop_request(self):
        response_dict = self._service.users().stop(userId='me').execute()
        if response_dict == '':
            print("Request to stop pushnotifications: Succesfull!")
        else:
            print("Request to stop push notifications failed.")
    def get_label_list(self):
        results = self._service.users().labels().list(userId="me").execute()
        return results.get("labels", [])
    def get_message(self, Id: str):
        try: 
            message = self._service.users().messages().get(userId="me", id=Id).execute()
        except HttpError:
            print(f"HttpError: {HttpError}\n when trying to get message with message ID: {Id}")
            message = ''
        return message
    def get_subject_from_id(self, message_id):
        pass
    def get_messages(self):
        return self._service.users().messages().list(userId="me", includeSpamTrash = False).execute()
    def get_history_list(self, list_path ,historyId):
        self.historylist = self._service.users().history().list(userId='me',startHistoryId=historyId, historyTypes = ["messageAdded","labelAdded"]).execute()
        self._save_history_list(list_path)
        self._get_ids_from_history_list()
    def search_history_list_subject(self, subject: str):
        if "history" not in self.historylist:
            return ""
        for historyId in self.historylist['history']:
            for message in historyId['messages']:
                msg = self.get_message(message['id'])
                if 'payload' in msg:
                    sender = ""
                    message_subject_id = ""
                    for header in msg['payload']['headers']:
                        if header['name'] == 'From':
                            sender = header['value']
                        if header['name'] == 'Subject' and header['value'].lower() == subject.lower():
                            message_subject_id = message['id']
                        if sender != "" and message_subject_id != "":
                            print(f"From: {sender} message received with subject: {subject} and id: {message_subject_id}")
                            return message_subject_id
        return ""
    def get_attachment_ids(self, message_id):
        msg = self.get_message(message_id)
        payload = msg['payload']
        for body in payload:
            if 'attachmentId' in body:
                return body['attachmentId']
            for part in payload['parts']:
                if 'attachmentId' in part['body']:
                    return part['body']['attachmentId']
    def get_attachment(self, path, message_id, attachment_id):
        att = self._service.users().messages().attachments().get(userId='me', messageId=message_id, id=attachment_id).execute()
        data = att['data']
        file_data = base64.urlsafe_b64decode(data)

        with open(path, 'wb') as f:
            f.write(file_data)
    def _search_name_in_payload(self, payload):
        for part in payload['parts']:
            if part['filename'] != '':
                return part['filename']
    def get_attachment_name(self, message_id, attachment_id):
        msg = self.get_message(message_id)
        payload = msg['payload']
        return self._search_name_in_payload(payload)

    def _get_ids_from_history_list(self):
        for history_id in self.historylist['history']:
            self._history_id_list.append(history_id)
            for message in history_id['messages']:
                self._history_message_list.append(message['id'])

    def get_subjects_from_history_list(self):
        for history_id in self._history_id_list:
            for message in history_id['messages']:
                msg = self.get_message(message['id'])
                for header in msg['payload']['headers']:
                            if header['name'] == 'Subject':
                                print(f"Message subject: {header['value']}")