import os


ID = "id"
MESSAGE = "message"
CHAT = "chat"
FROM = "from"
TEXT = "text"
OK = "ok"
NEW_CHAT_PARTICIPANT = "new_chat_participant"
USERNAME = "username"
NEW_CHAT_TITLE = "new_chat_title"
USER = "user"
USER_CHAT = "User chat"
UPADTING = "Updating"
CREATING = "Creating"
WEBHOOK_URL = "https://f784fbaa700a.ngrok.io/listen_msg"
WEBHOOK_END = "Webhook call end"


# Response Messages
CREATE_UPDATE_MSG = "%s the %s data record: %s"
INVALID_MSG = "Could not save the %s data, Invalid data"
DATA_SAVED = "%s data saved"

# Environment Variables
BOT_TOKEN = os.environ["TOKEN"]
BOT_USERNAME = os.environ["BOT_USERNAME"]

# Telegram Events
TELEGRAM_EVENTS = {
    "new_chat_participant",
    "new_chat_title",
    "text",
}