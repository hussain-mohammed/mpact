import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot.settings")
django.setup()

from telethon import TelegramClient, events
from telethon.tl import types

from constants import BOT_TOKEN, TELEGRAM_API_HASH, TELEGRAM_API_ID
from logger import logger
from mpact.models import Bot, Chat, Individual
from mpact.serializers import ChatSerializer
from utils import get_or_none

bot_client = TelegramClient("bot", TELEGRAM_API_ID, TELEGRAM_API_HASH).start(
    bot_token=BOT_TOKEN
)


@bot_client.on(events.NewMessage)
async def msg_handler(event):
    """
    Event handler for new message
    """
    try:
        if event.message.message == "/start":
            # check if the message is from individual(PeerUser) or group(PeerChat) chat
            if isinstance(event.message.peer_id, types.PeerUser):
                current_bot = await bot_client.get_me()
                user_details = await bot_client.get_entity(
                    event.message.peer_id.user_id
                )
                bot_inst = Bot.objects.get(bot_id=current_bot.id)
                Individual.objects.create(
                    bot=bot_inst,
                    individual_id=user_details.id,
                    username=user_details.username,
                    first_name=user_details.first_name,
                    last_name=user_details.last_name,
                )
                await event.reply("Welcome! How may i help you?")

    except Exception as exception:
        logger.exception(exception)


@bot_client.on(events.ChatAction)
async def chat_handler(event):
    """
    Event handler for chat action such as chat created, user added, user joined and new title
    """
    try:
        if event.created:
            data = {
                "chat_id": event.action_message.peer_id.chat_id,
                "title": event.new_title,
                "created_at": event.action_message.date,
            }
            serializer = ChatSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            # add newly created group details in the database
            chat = Chat.objects.create(**data)
            for user in event.action_message.action.users:
                user_details = await bot_client.get_entity(user)
                current_bot = await bot_client.get_me()

                if user_details.username == current_bot.username:
                    # add bot details in the database
                    bot = Bot.objects.create(
                        chat=chat,
                        bot_id=user_details.id,
                        username=user_details.username,
                        first_name=user_details.first_name,
                        last_name=user_details.last_name,
                    )
                    bot.save()

        elif event.new_title:
            chat = get_or_none(Chat, chat_id=event.action_message.peer_id.chat_id)
            if chat:
                chat.title = event.new_title
                chat.save()

    except Exception as exception:
        logger.exception(exception)


def main():
    """Start the bot."""
    with bot_client:
        bot_client.run_until_disconnected()


if __name__ == "__main__":
    main()
