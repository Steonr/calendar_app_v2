from abc import ABC, abstractmethod
import concurrent.futures

from google.cloud import pubsub_v1
def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()
    return message


class SubscriberClient:
    def __init__(self):
        self._project_id = "myproject-266417"
        self._topic_id = "checkGmail"
        self._sub_id = "checkGmail"
        self._sub_client = pubsub_v1.SubscriberClient()
        self._sub_path = self._sub_client.subscription_path(self._project_id, self._sub_id)
        self._topic_path = self._sub_client.topic_path(self._project_id, self._topic_id)
        self._message = pubsub_v1.subscriber.message.Message
        self._service_account = "Calendar@myproject-266417.iam.gserviceaccount.com"
        self._policy = self._sub_client.get_iam_policy(request={"resource": self._sub_path})

    def create_subscription(self):
        return self._sub_client.create_subscription(request=self._request)

    def _get_policy(self):
        print(f"Policy for subscription {self._sub_path}:")
        try:
            for binding in self._policy.bindings:
                print(f"Role: {binding.role}, Members: {binding.member}")
        except TimeoutError:
            print(f"TimeoutError: {TimeoutError}")

    def _set_policy(self):
        
        # Add all users as subscriber.
        self._policy.bindings.add(
            role="roles/pubsub.publisher", members=["serviceAccount:Calendar@myproject-266417.iam.gserviceaccount.com"]
        )
        # Set the policy
        self._policy = self._sub_client.set_iam_policy(request={"resource": self._topic_path, "policy": self._policy})
        print(f"IAM policy for topic {self._topic_id} set: {self._policy}")

    def streaming_pull(self, timeout = 5.0) -> None:
        ''' When `timeout` is not set, result() will block indefinitely
        Args:
            timeout (int): seconds 
        Returns:
            None
        '''
        streaming_pull_future = self._sub_client.subscribe(self._sub_path, callback=callback)
        print(f"Listening for messages on {self._sub_path}..\n")
        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with self._sub_client:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                streaming_pull_future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                print(f"Streaming pull, timed out after {timeout} seconds")
                streaming_pull_future.cancel()  # Trigger the shutdown.
                streaming_pull_future.result()  # Block until the shutdown is complete.

            finally:
                self._sub_client.close()
    def get_permissions(self):
        permissions_to_check = [
            "pubsub.subscriptions.consume",
            "pubsub.subscriptions.update",
        ]

        allowed_permissions = self._sub_client.test_iam_permissions(
            request={"resource": self._sub_path, "permissions": permissions_to_check}
        )
        print(f"Allowed permissions for subscription {self._sub_path}: {allowed_permissions}")
        self._sub_client.close()