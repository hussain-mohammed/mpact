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
    WEBHOOK_URL = "https://8a7e5dd2d909.ngrok.io/listen_msg"