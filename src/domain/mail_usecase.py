from interfaces.mail_interface import MailInterface


class MailListenerUsecase(MailInterface):
    def __init__(self):
        pass


    def listen_to_inbox(self):
        while True:
            MailInterface.listen_to_inbox()
            if mail:
                return