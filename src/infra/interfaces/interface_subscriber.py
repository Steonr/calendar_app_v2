from abc import ABC, abstractmethod
class ISubscriber(ABC):
    def __init__(self):
        pass
    def _callback(self) -> None:
        pass
    def create_subscription(self):
        pass
    def pull_message(self):
        pass
    def streaming_pull(self, file_path, timeout = 5.0) -> None:
        pass
    def get_messages(self):
        pass