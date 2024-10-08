from domain.entities.gmail import Response

import json
import time
from abc import ABC, abstractmethod
import concurrent.futures

from google.api_core import retry
from google.cloud import pubsub_v1

def save_data(self, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

class SubscriberClient:
    def __init__(self):
        self._message = ""
        self._messages = []
        self._project_id = "myproject-266417"
        self._topic_id = "checkGmail"
        self._sub_id = "checkGmail"
        self._service_account = "Calendar@myproject-266417.iam.gserviceaccount.com"

    def _callback(self, message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message}.")
        message.ack()

    def create_subscription(self):
        return self._sub_client.create_subscription(request=self._request)

    def pull_message(self):
        self._sub_client = pubsub_v1.SubscriberClient()
        self._sub_path = self._sub_client.subscription_path(self._project_id, self._sub_id)

        NUM_MESSAGES = 1

        # Wrap the subscriber in a 'with' block to automatically call close() to
        # close the underlying gRPC channel when done.
        with self._sub_client:
            # The subscriber pulls a specific number of messages. The actual
            # number of messages pulled may be smaller than max_messages.
            response = self._sub_client.pull(
                request={"subscription": self._sub_path, "max_messages": NUM_MESSAGES},
                retry=retry.Retry(deadline=300),
            )

            ack_ids = []
            for received_message in response.received_messages:
                self._message = json.loads(received_message.message.data)
                print(f"Received: {self._message}.")
                ack_ids.append(received_message.ack_id)
            if ack_ids:
                # Acknowledges the received messages so they will not be sent again.
                self._sub_client.acknowledge(request={"subscription": self._sub_path, "ack_ids": ack_ids})
                print(f"Received and acknowledged {len(response.received_messages)} message(s) from {self._sub_path}.")
        message = self._message['historyId'] if 'historyId' in self._message else ""
        return message
    def streaming_pull(self, file_path, timeout = 5.0) -> None:
        ''' When `timeout` is not set, result() will block indefinitely
        Args:
            timeout (int): seconds 
        Returns:
            None
        '''
        self._file_path = file_path
        self._sub_client = pubsub_v1.SubscriberClient()
        self._sub_path = self._sub_client.subscription_path(self._project_id, self._sub_id)
        self._topic_path = self._sub_client.topic_path(self._project_id, self._topic_id)
        self.streaming_pull_future = self._sub_client.subscribe(self._sub_path, callback=self._callback)
        print(f"Listening for messages on {self._sub_path}..\n")
        with self._sub_client:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                self.streaming_pull_future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                print(f"Streaming pull, timed out after {timeout} seconds")
                self.streaming_pull_future.cancel()  # Trigger the shutdown.
                self.streaming_pull_future.result()  # Block until the shutdown is complete.
    def get_messages(self):
        return self._messages