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