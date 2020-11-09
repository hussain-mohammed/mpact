import os


class Constants:
    ID = "id"
    MESSAGE = "message"
    CHAT = "chat"
    FROM = "from"
    TEXT = "text"
    OK = "ok"
    NEW_CHAT_PARTICIPANT = "new_chat_participant"
    USERNAME = "username"
    BOT_USERNAME = os.environ.get("BOT_USERNAME")
    NEW_CHAT_TITLE = "new_chat_title"
    BOT_TOKEN = os.environ.get("TOKEN")
    WEBHOOK_URL = "https://f784fbaa700a.ngrok.io/listen_msg"


WEBHOOK_END = "Webhook call end"
CREATE_UPDATE_MSG = "%s the %s data record: %s"
INVALID_MSG = "Could not save the %s data, Invalid data"
DATA_SAVED = "%s data saved"
USER = "user"
USER_CHAT = "User chat"
UPADTING = "Updating"
CREATING = "Creating"