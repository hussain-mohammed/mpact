from contextlib import asynccontextmanager

from constants import (
    BOT_TOKEN,
    CHAT_ID,
    CODE,
    DATA,
    FIRST_NAME,
    INVALID_CODE,
    IS_SUCCESS,
    LAST_NAME,
    LOGOUT,
    MESSAGE,
    MESSAGE_SENT,
    NOT_AUTHORIZED,
    PASSWORD,
    PASSWORD_REQUIRED,
    PHONE,
    PHONE_CODE_HASH,
    PHONE_NOT_REGISTERED,
    STATUS,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
    TWO_FA_ENABLED,
    USERNAME,
)
from django.contrib.auth.models import User
from logger import logger
from rest_framework import status
from telethon import TelegramClient, functions
from telethon.errors import (
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
)
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
        NOT_AUTHORIZED[DATA][MESSAGE] = PHONE_NOT_REGISTERED
        return NOT_AUTHORIZED

    async with get_anon_client() as client:
        if PASSWORD in data:
            return await two_factor_auth(client, data)
        elif CODE in data:
            return await validate_code(client, data)
        # sending otp to phone number
        code_request = await client.send_code_request(data[PHONE])
        return {
            DATA: {PHONE_CODE_HASH: code_request.phone_code_hash, IS_SUCCESS: True},
            STATUS: status.HTTP_200_OK,
        }


async def two_factor_auth(client, data):
    """
    Verify the password entered by the user and
    returns the user details upon successful login
    """
    user_details = await client.sign_in(
        password=data[PASSWORD],
    )
    await client.disconnect()
    return {
        DATA: {
            FIRST_NAME: user_details.first_name,
            LAST_NAME: user_details.last_name,
            USERNAME: user_details.username,
            IS_SUCCESS: True,
        },
        STATUS: status.HTTP_200_OK,
    }


async def validate_code(client, data):
    """
    validate the code (OTP) & return user details and if two factor authenticated
    is enabled, it will ask for password.
    """
    try:
        user_details = await client.sign_in(
            phone=data[PHONE],
            code=data[CODE],
            phone_code_hash=data[PHONE_CODE_HASH],
        )
    except SessionPasswordNeededError:
        return {
            DATA: {MESSAGE: PASSWORD_REQUIRED, TWO_FA_ENABLED: True, IS_SUCCESS: True},
            STATUS: status.HTTP_200_OK,
        }
    except (PhoneCodeInvalidError, PhoneCodeExpiredError):
        return {
            DATA: {MESSAGE: INVALID_CODE, IS_SUCCESS: False},
            STATUS: status.HTTP_400_BAD_REQUEST,
        }
    await client.disconnect()
    return {
        DATA: {
            FIRST_NAME: user_details.first_name,
            LAST_NAME: user_details.last_name,
            USERNAME: user_details.username,
            IS_SUCCESS: True,
        },
        STATUS: status.HTTP_200_OK,
    }


async def logout():
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            await client.log_out()
    return {
        DATA: {MESSAGE: LOGOUT, IS_SUCCESS: True},
        STATUS: status.HTTP_200_OK,
    }


async def send_msg(data):
    """
    Sends the message to the particular chat
    """
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            async with await start_bot_client() as bot:
                await bot.send_message(data[CHAT_ID], data[MESSAGE])
            return {
                DATA: {MESSAGE: MESSAGE_SENT},
                STATUS: status.HTTP_200_OK,
                IS_SUCCESS: True,
            }
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
