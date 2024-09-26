from googleapiclient.discovery import build

request = {
  'labelIds': ['INBOX'],
  'topicName': 'projects/myproject-266417/topics/checkGmail'
}

class GmailApi:
    def __init__(self, SubscriberClient, credentials):
        self._service = build("gmail", "v1", credentials=credentials)
    def request(self):
        return self._service.users().watch(userId='me', body=request).execute()
    def get_label_list(self):
        results = self._service.users().labels().list(userId="me").execute()
        return results.get("labels", [])
    