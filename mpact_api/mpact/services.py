from telegram.ext import Updater

from . import constants
from .logger import logger
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
        logger.debug(
            constants.CREATE_UPDATE_MSG, constants.UPADTING, constants.CHAT, chat_data
        )
        chat_serializer = ChatDataSerializer(chat_instance, data=chat_data)
    else:
        # To create a new record
        logger.debug(
            constants.CREATE_UPDATE_MSG, constants.CREATING, constants.CHAT, chat_data
        )
        chat_serializer = ChatDataSerializer(data=chat_data)
    if chat_serializer.is_valid():
        chat_serializer.save()
        logger.debug(constants.DATA_SAVED, constants.CHAT)
        return True
    logger.debug(constants.INVALID_MSG, constants.CHAT)
    return False


def save_userdata(userdata):
    logger.debug(
        constants.CREATE_UPDATE_MSG, constants.CREATING, constants.USER, userdata
    )
    user_serializer = UserDataSerializer(data=userdata)
    if user_serializer.is_valid():
        user_data_rec = UserData.objects.create(**userdata)
        user_data_rec.save()
        logger.debug(constants.DATA_SAVED, constants.USER)
        return user_data_rec
    logger.debug(constants.INVALID_MSG, constants.USER)
    return False


def save_userchat(chat_data, user_data_inst):
    user_chat_record = UserChat.objects.create(
        chat_id=chat_data.get(constants.ID), user_id=user_data_inst
    )
    user_chat_record.save()
    logger.debug(constants.DATA_SAVED, constants.USER_CHAT)
    return True
