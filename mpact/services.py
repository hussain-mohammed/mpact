from django.contrib.auth.models import User
from django.http import HttpResponse
from telethon import TelegramClient

from .constants import (
    BOT_TOKEN,
    CHAT_ID,
    CODE,
    LOGOUT,
    MESSAGE,
    MESSAGE_SENT,
    NOT_AUTHORIZED,
    PHONE,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
)
from .logger import logger


def get_anon_client() -> TelegramClient:
    """
    Returns a TelegramClient with the session name "anon"
    """
    return get_telegram_client("anon")


def start_bot_client() -> TelegramClient:
    """
    Returns a TelegramClient for bot
    """
    return get_telegram_client("bot").start(bot_token=BOT_TOKEN)


def get_telegram_client(session_name: str) -> TelegramClient:
    return TelegramClient(session_name, TELEGRAM_API_ID, TELEGRAM_API_HASH)


def exception(func):
    def inner_function(*args, **kwargs):
        try:
            results = func(*args, **kwargs)
            return HttpResponse(results)
        except Exception as exception:
            logger.exception(exception)
            raise

    return inner_function


async def login(data):
    """
    Returns the logged in user details or hash code & other details for code request
    """
    user = get_or_none(User, profile__phone=data[PHONE])
    if not user:
        return "Phone Number is not registered."
    client = get_anon_client()
    await client.connect()
    if CODE in data:
        user_details = await client.sign_in(
            phone=data[PHONE], code=data[CODE], phone_code_hash=data["phone_code_hash"]
        )
        await client.disconnect()
        return user_details
    # sending otp to phone number
    code_request = await client.send_code_request(data[PHONE])
    await client.disconnect()
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
            dialogs = await client.get_dialogs()
            return dialogs
        return NOT_AUTHORIZED


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
