from telegram.ext import Updater

from . import constants
from .models import UserChat, UserData
from .serializers import ChatDataSerializer, UserDataSerializer

updater = Updater(constants.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def set_webhook():
    # TODO: we can move this to config file or keep this as a seperate script.
    webhook = updater.bot.setWebhook(
        constants.WEBHOOK_URL, allowed_updates=[constants.MESSAGE]
    )
    return webhook  # returns True or False


def save_chatdata(chat_data, chat_instance=None):
    if chat_instance:
        # To update already existing record
        chat_serializer = ChatDataSerializer(chat_instance, data=chat_data)
    else:
        # To create a new record
        chat_serializer = ChatDataSerializer(data=chat_data)
    if chat_serializer.is_valid(raise_exception=True):
        chat_serializer.save()


def save_userdata(userdata):
    user_serializer = UserDataSerializer(data=userdata)
    if user_serializer.is_valid(raise_exception=True):
        user_data_rec = UserData.objects.create(**userdata)
        user_data_rec.save()
        return user_data_rec


def save_userchat(chat_data, user_data_inst):
    user_chat_record = UserChat.objects.create(
        chat_id=chat_data.get(constants.ID), user_id=user_data_inst
    )
    user_chat_record.save()
