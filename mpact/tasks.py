from celery import shared_task
from channels.layers import get_channel_layer
from telegram_bot.constants import (
    DATA,
    FROM_GROUP,
    IS_SUCCESS,
    MESSAGE,
    MESSAGE_SENT,
    ROOM_ID,
    SENDER_ID,
    SENDER_NAME,
    TELEGRAM_MSG_ID,
    WEBSOCKET_ROOM_NAME,
)
from telethon.tl.types import InputPeerChat, InputPeerUser

from .models import Chat, Individual
from .serializers import MessageSerializer
from .services import start_bot_client
from .views import new_or_current_event_loop


@shared_task
def send_msgs(receiver_id, message):
    return new_or_current_event_loop().run_until_complete(
        send_msg(receiver_id, message)
    )


async def send_msg(receiver_id, message):
    """
    Sends the message to the particular chat
    """
    async with await start_bot_client() as bot:
        data = {}
        current_bot = await bot.get_me()
        data[SENDER_ID] = current_bot.id
        data[SENDER_NAME] = current_bot.first_name
        data[ROOM_ID] = receiver_id
        data[MESSAGE] = message
        try:
            group_chat = Chat.objects.get(id=receiver_id)
            data[FROM_GROUP] = True

        except Chat.DoesNotExist:
            individual_chat = Individual.objects.get(id=receiver_id)
            data[FROM_GROUP] = False

        if data[FROM_GROUP]:
            receiver = InputPeerChat(int(data[ROOM_ID]))
        else:
            access_hash = individual_chat.access_hash
            receiver = InputPeerUser(int(data[ROOM_ID]), int(access_hash))

        msg_inst = await bot.send_message(receiver, data[MESSAGE])
        data[TELEGRAM_MSG_ID] = msg_inst.id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                WEBSOCKET_ROOM_NAME, {"type": "chat_message", MESSAGE: serializer.data}
            )

    return {
        DATA: {MESSAGE: MESSAGE_SENT},
        IS_SUCCESS: True,
    }
