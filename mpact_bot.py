import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot.settings")
django.setup()

from channels.layers import get_channel_layer
from telethon import TelegramClient, events
from telethon.tl import types

from mpact.models import Bot, BotIndividual, Chat, ChatBot, Individual
from mpact.serializers import ChatSerializer, MessageSerializer
from telegram_bot.constants import (
    BOT_TOKEN,
    MESSAGE,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
    WEBSOCKET_ROOM_NAME,
)
from telegram_bot.logger import logger
from telegram_bot.messages import WELCOME
from telegram_bot.utils import get_or_none

bot_client = TelegramClient("bot", TELEGRAM_API_ID, TELEGRAM_API_HASH).start(
    bot_token=BOT_TOKEN
)


@bot_client.on(events.ChatAction)
async def chat_handler(event):
    """
    Event handler for chat action such as chat created, user added, user joined and new title
    """
    try:
        if event.created:
            data = {
                "id": event.action_message.peer_id.chat_id,
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
                    bot, created = Bot.objects.get_or_create(
                        id=user_details.id,
                        defaults={
                            "username": user_details.username,
                            "first_name": user_details.first_name,
                            "last_name": user_details.last_name,
                        },
                    )
                    chat_bot = ChatBot.objects.create(chat=chat, bot=bot)
                    chat_bot.save()

        elif event.new_title:
            chat = get_or_none(Chat, id=event.action_message.peer_id.chat_id)
            if chat:
                chat.title = event.new_title
                chat.save()

    except Exception as exception:
        logger.exception(exception)


@bot_client.on(events.NewMessage(incoming=True))
async def incoming_message_handler(event):
    """
    Event handler for all the incoming messages
    """
    try:
        channel_layer = get_channel_layer()
        msg_data = message_data(event.sender.id, event.sender.id, event.text)

        # check if the message is from individual(PeerUser) or group(PeerChat) chat
        if isinstance(event.message.peer_id, types.PeerUser):
            await save_send_message(msg_data, channel_layer)
            serializer = MessageSerializer(data=msg_data)

            if event.text == "/start":
                await start_handler(event, channel_layer)

        elif isinstance(event.message.peer_id, types.PeerChat):
            msg_data["id"] = event.message.id
            msg_data["date"] = str(event.message.date)
            await channel_layer.group_send(
                WEBSOCKET_ROOM_NAME,
                {"type": "chat_message", MESSAGE: msg_data},
            )

    except Exception as exception:
        logger.exception(exception)


async def start_handler(event, channel_layer):
    """
    Handler for "/start"
    """
    current_bot = await bot_client.get_me()
    user_details = await bot_client.get_entity(event.message.peer_id.user_id)

    bot = Bot.objects.get(id=current_bot.id)

    individual, i_created = Individual.objects.get_or_create(
        id=user_details.id,
        defaults={
            "username": user_details.username,
            "first_name": user_details.first_name,
            "last_name": user_details.last_name,
            "access_hash": user_details.access_hash,
        },
    )

    bot_individual, bi_created = BotIndividual.objects.get_or_create(
        bot=bot, individual=individual
    )
    if bi_created:
        bot_individual.save()

    await event.reply(WELCOME)
    msg_data = message_data(individual.id, current_bot.id, WELCOME)
    await save_send_message(msg_data, channel_layer)


def message_data(individual_id, sender_id, message):
    return {
        "individual": individual_id,
        "sender": sender_id,
        "message": message,
    }


async def save_send_message(msg_data, channel_layer):
    """Save the message to the database and
    send to the connected websockets client"""

    serializer = MessageSerializer(data=msg_data)
    if serializer.is_valid():
        serializer.save()
        await channel_layer.group_send(
            WEBSOCKET_ROOM_NAME,
            {"type": "chat_message", MESSAGE: serializer.data},
        )


def main():
    """Start the bot."""
    with bot_client:
        bot_client.run_until_disconnected()


if __name__ == "__main__":
    main()
