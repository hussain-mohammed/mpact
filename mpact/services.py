from contextlib import asynccontextmanager

from constants import (
    BOT_TOKEN,
    CHAT_ID,
    CODE,
    DATA,
    IS_SUCCESS,
    LOGOUT,
    MESSAGE,
    MESSAGE_SENT,
    NOT_AUTHORIZED,
    PHONE,
    STATUS,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
)
from django.contrib.auth.models import User
from logger import logger
from rest_framework import status
from telethon import TelegramClient, functions
from utils import get_or_none

from .models import ChatData


@asynccontextmanager
async def get_anon_client():
    """
    TelegramClient is already an async context manager. This context
    manager connect to the telegram and logs exceptions.
    """
    try:
        client = get_telegram_client("anon")
        await client.connect()
        yield client
    except Exception as exception:
        logger.exception(exception)
        raise
    finally:
        await client.disconnect()


def start_bot_client() -> TelegramClient:
    """
    Returns a TelegramClient for bot
    """
    return get_telegram_client("bot").start(bot_token=BOT_TOKEN)


def get_telegram_client(session_name: str) -> TelegramClient:
    return TelegramClient(session_name, TELEGRAM_API_ID, TELEGRAM_API_HASH)


async def login(data):
    """
    Returns the logged in user details or hash code & other details for code request
    """
    user = get_or_none(User, profile__phone=data[PHONE])
    if not user:
        return "Phone Number is not registered in our system."

    async with get_anon_client() as client:
        if CODE in data:
            user_details = await client.sign_in(
                phone=data[PHONE],
                code=data[CODE],
                phone_code_hash=data["phone_code_hash"],
            )
            await client.disconnect()
            return user_details
        # sending otp to phone number
        code_request = await client.send_code_request(data[PHONE])
        return code_request


async def logout():
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            await client.log_out()
    return LOGOUT


async def send_msg(data):
    """
    Sends the message to the particular chat
    """
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            async with await start_bot_client() as bot:
                await bot.send_message(data[CHAT_ID], data[MESSAGE])
            return MESSAGE_SENT
        return NOT_AUTHORIZED


async def get_dialog():
    """
    Returns dialogs if the user is authorized
    """
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            return await bulid_json(client)
        return NOT_AUTHORIZED


async def bulid_json(client):
    dialogs = ChatData.objects.all()
    dialogs_json = []
    for dialog in dialogs:
        temp_dialog = {}
        temp_dialog[CHAT_ID] = dialog.chat_id
        temp_dialog["title"] = dialog.title
        peer_details = await client(
            functions.messages.GetPeerDialogsRequest(peers=[int(dialog.chat_id)])
        )
        temp_dialog["unread_count"] = peer_details.dialogs[0].unread_count

        msgs = await client.get_messages(int(dialog.chat_id))
        temp_dialog[MESSAGE] = msgs[0].message

        user = await client.get_entity(msgs[0].from_id.user_id)
        temp_dialog["first_name"] = user.first_name
        dialogs_json.append(temp_dialog)

    return {
        DATA: {"dialogs": dialogs_json, IS_SUCCESS: True},
        STATUS: status.HTTP_200_OK,
    }
