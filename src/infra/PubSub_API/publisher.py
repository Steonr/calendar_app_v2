from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable

def get_callback(publish_future: pubsub_v1.publisher.futures.Future, data: str) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
        def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
            try:
                # Wait 60 seconds for the publish call to succeed.
                print(publish_future.result(timeout=60))
            except futures.TimeoutError:
                print(f"Publishing {data} timed out.")
        return callback



class PublisherClient:
    def __init__(self):
        self._project_id = "myproject-266417"
        self._topic_id = "checkGmail"
        self._pub_id = "checkGmail"
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
        
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(self._project_id, self._topic_id)
        publish_futures = []

        for i in range(10):
            data = str(i)
            # When you publish a message, the client returns a future.
            publish_future = publisher.publish(topic_path, data.encode("utf-8"))
            # Non-blocking. Publish failures are handled in the callback function.
            publish_future.add_done_callback(get_callback(publish_future, data))
            publish_futures.append(publish_future)

        # Wait for all the publish futures to resolve before exiting.
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        print(f"Published messages with error handler to {topic_path}.")


