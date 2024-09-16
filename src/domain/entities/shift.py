""" this class has the definition of the shift entity
"""
from dataclasses import dataclass, asdict
from src.domain.value_objects import ShiftId

import datetime

@dataclass
class Shift:
    shift_id: ShiftId
    name: str
    start_time: datetime
    end_time: datetime
    description: str

    @classmethod
    def from_dict(cls, data):
        """ convert data from a dictionary
        """
        return cls(**data)
    
    def to_dict(self):
        """ convert data into dictionary
        """
        return asdict(self)