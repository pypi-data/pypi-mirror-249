import os

# import vonage
from dotenv import load_dotenv
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from message_local.MessageLocal import MessageLocal

WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_ID = 173
WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_NAME = 'send whatsapp-message-local-python-package'

whatsapp_message_local_python_unit_tests_logger_object = {
    'component_id': WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": "jenya.b@circ.zone"
}

logger = Logger.create_logger(
    object=whatsapp_message_local_python_unit_tests_logger_object)
WHATSAPP_MESSAGE_VONAGE_API_TYPE_ID = 9
load_dotenv()


class VonageWhatsAppMessagesLocal(MessageLocal):
    """Assuming the usage is as follows:
    message_local = MessageLocal(...)
    message_local.__class__ = WhatsAppMessageInforuLocal
    message_local.__init__()  # calling the "init" of WhatsAppMessageInforuLocal
    message_local.send(...)  # calling the "send" of WhatsAppMessageInforuLocal
    """
    def __init__(self, default_from_number: str, to_number: str) -> None:  # noqa
        # Don't call super().__init__(), we already have the message_local object
        self.api_key = os.getenv("VONAGE_API_KEY")
        self.api_secret = os.getenv("VONAGE_API_SECRET")
        self.default_from_number = default_from_number
        self.to_number = to_number
        self._api_type_id = WHATSAPP_MESSAGE_VONAGE_API_TYPE_ID  # used by MessageLocal
        self.url = "https://messages-sandbox.nexmo.com/v1/messages"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        # self.vonage = vonage.Messages(client=vonage.Client(key=self.api_key, secret=self.api_secret))

    def send(self, person_id: int, message: str) -> None:
        """send message use vonage api"""
        logger.start("send message to phone by id ", object={
            "profile_id": person_id, 'message': message})
        data = {
            "from": self.default_from_number,
            "to": self.to_number,
            "message_type": "text",
            "text": message,
            "channel": "whatsapp"
        }
        # if (os.getenv("REALLY_SEND_WHATSAPP") and
        #       self.can_send(api_data=data, outgoing_body=data)):

        # self.after_send_attempt(outgoing_body=payload,
        #                                         incoming_message=response.json(),
        #                                         http_status_code=response.status_code,
        #                                         response_body=response.text)
        logger.end()
