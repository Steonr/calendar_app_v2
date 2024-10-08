from dataclasses import dataclass, asdict
import json
@dataclass
class ResponsModel:
    historyId: str
    expiration: str
    @classmethod
    def from_dict(cls, data):
        ''' convert data from dictionary
        '''
        return cls(**data)
    def to_dict(self):
        ''' convert data to dictionary
        '''
        return asdict(self)

    def save_data(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

@dataclass
class PullMessage:
    historyId: str
    expiration: str
    @classmethod
    def from_dict(cls, data):
        ''' convert data from dictionary
        '''
        return cls(**data)
    def to_dict(self):
        ''' convert data to dictionary
        '''
        return asdict(self)

@dataclass
class HistoryList:
    def __init__(self):
        self.data = {}
        self.current_historyId = ''
        self.old_historyId = ''
        self.last_message = ''
        self.messages_ids = []
    @classmethod
    def from_dict(cls, data):
        ''' convert data from dictionary
        '''
        return cls(**data)
    def to_dict(self):
        ''' convert data to dictionary
        '''
        return asdict(self)
    def save_data(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    def set_historyId(self, history_Id):
        if self.current_historyId != '':
            self.old_historyId = self.current_historyId
        self.current_historyId = history_Id
    def get_historyId(self):
        return self.current_historyId
    def get_last_message(self):
        try: 
            self.last_message = self.data['messages'][0]['id']
        except Exception:
            self.last_message = None
    def get_messages_ids(self, history_id):
        if 'history' in self.data:
            for hist_id in self.data['history']:
                for message in hist_id['messages']:
                        self.messages_ids.append(message['id'])

@dataclass
class Message:
    def __init__(self):
        self.data = {}
    @classmethod
    def from_dict(cls, data):
        ''' convert data from dictionary
        '''
        return cls(**data)
    def to_dict(self):
        ''' convert data to dictionary
        '''
        return asdict(self)
    def get_title(self):
        return next(
            (
                part['value']
                for part in self.data['payload']['headers']
                if part['name'] == 'Subject'
            ),
            None,
        )
    def get_snippet(self):
        return self.data['snippet']
    def get_attachmentId(self):
        pass
    def save_data(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
