from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()


class SubscriberClient:
    def __init__(self):
        self._project_id = "myproject-266417"
        self._topic_id = "checkGmail"
        self._sub_id = "checkGmail"
        self._service_account = "Calendar@myproject-266417.iam.gserviceaccount.com"

    def _get_policy(self):
        pass

    def _set_policy(self):
        pass

    def get_permissions(self):
        pass

    def streaming_push(self, timeout = 5.0) -> None:
        ''' When `timeout` is not set, result() will block indefinitely
        Args:
            timeout (int): seconds 
        Returns:
            None
        '''


