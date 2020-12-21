import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot.settings")
django.setup()

from telethon import TelegramClient, events

from constants import BOT_TOKEN, TELEGRAM_API_HASH, TELEGRAM_API_ID
from logger import logger
from mpact.models import ChatData
from mpact.serializers import ChatDataSerializer
from utils import get_or_none

bot = TelegramClient("bot", TELEGRAM_API_ID, TELEGRAM_API_HASH).start(
    bot_token=BOT_TOKEN
)


@bot.on(events.ChatAction)
async def handler(event):
    """
    Event handler for chat action such as chat created, user added, user joined and new title
    """
    try:
        if event.created:
            chat_details = await bot.get_entity(event.action_message.peer_id.chat_id)
            data = {
                "chat_id": chat_details.id,
                "title": chat_details.title,
                "created_at": chat_details.date,
            }
            serializer = ChatDataSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        elif event.new_title:
            chat = get_or_none(ChatData, chat_id=event.action_message.peer_id.chat_id)
            if chat:
                chat.title = event.new_title
                chat.save()

    except Exception as exception:
        logger.exception(exception)


def main():
    """Start the bot."""
    with bot:
        bot.run_until_disconnected()


if __name__ == "__main__":
    main()
