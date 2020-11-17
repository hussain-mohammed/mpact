import os


ID = "id"
MESSAGE = "message"
CHAT = "chat"
FROM = "from"
OK = "ok"
USERNAME = "username"
USER = "user"
USER_CHAT = "User chat"
UPADTING = "Updating"
CREATING = "Creating"
WEBHOOK_URL = "https://f784fbaa700a.ngrok.io/listen_msg"
IS_DELETED = "is_deleted"

# Response Messages
CREATE_UPDATE_MSG = "%s the %s data record: %s"
INVALID_MSG = "Could not save the %s data, Invalid data"
DATA_SAVED = "%s data saved"

# Environment Variables
BOT_TOKEN = os.environ["TOKEN"]
BOT_USERNAME = os.environ["BOT_USERNAME"]

# Telegram Events
TEXT = "text"
NEW_CHAT_PARTICIPANT = "new_chat_participant"
NEW_CHAT_TITLE = "new_chat_title"
LEFT_CHAT_PARTICIPANT = "left_chat_participant"

ANON = "*" * 16
REPLACE = {
    "id": 0,
    "username": ANON,
    "first_name": ANON,
    "last_name": ANON,
    "language_code": "**",
}
