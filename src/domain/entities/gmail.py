from dataclasses import dataclass, asdict
import json
@dataclass
class Request:
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
class Response:
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
    def save(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)
    @classmethod
    def get_data(cls, response_path):   
        try:
            with open(response_path, 'rb') as f:
                data = json.load(f)
            return cls(**data)
        except FileNotFoundError:
            data = None
            return cls('', '')