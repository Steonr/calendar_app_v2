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
        self.last_message = ''
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

    def get_last_message(self):
        self.last_message = self.data['messages'][0]['id']


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
        return self.data['snippet']
    def get_attachmentId(self):
        pass
    def save_data(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
