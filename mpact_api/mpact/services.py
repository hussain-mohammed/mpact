from telethon import TelegramClient

from .constants import (
    BOT_TOKEN,
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

# Remember to use your own values from my.telegram.org!
api_id = TELEGRAM_API_ID
api_hash = TELEGRAM_API_HASH
bot_token = BOT_TOKEN
# loop = asyncio.get_event_loop()
client = TelegramClient("anon", api_id, api_hash)
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)


def connection(func):
    async def inner_function(*args, **kwargs):
        try:
            # Start the client before we start serving
            await client.connect()
            results = await func(*args, **kwargs)
            # After serving (near shutdown), clean up the client
            await client.disconnect()
            return results
        except Exception as exception:
            logger.exception(exception)
            raise

    return inner_function


@connection
async def login(data):
    if CODE in data:
        user_details = await client.sign_in(code=data[CODE])
        return user_details
    else:
        # sending otp to phone number
        code_request = await client.send_code_request(data[PHONE])
        return code_request


@connection
async def logout():
    if await client.is_user_authorized():
        await client.log_out()
    return LOGOUT


@connection
async def send_msg(data):
    if await client.is_user_authorized():
        await client.send_message(-488152794, data[MESSAGE])
    return MESSAGE_SENT


@connection
async def get_dialogs():
    if await client.is_user_authorized():
        dialogs = await client.get_dialogs()
        return dialogs
    return NOT_AUTHORIZED
