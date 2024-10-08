from abc import ABC, abstractmethod

class MailInterface(ABC):
    @abstractmethod
    def listen_to_inbox():
        pass    
