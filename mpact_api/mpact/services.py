from telegram.ext import Updater

from . import constants
from .constants import Constants
from .logger import logger
from .models import UserChat, UserData
from .serializers import ChatDataSerializer, UserDataSerializer

updater = Updater(Constants.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def set_webhook():
    # TODO: we can move this to config file or keep this as a seperate script.
    webhook = updater.bot.setWebhook(
        Constants.WEBHOOK_URL, allowed_updates=[Constants.MESSAGE]
    )
    return webhook  # returns True or False


def save_chatdata(chat_data, chat_instance=None):

    if chat_instance:
        # To update already existing record
        logger.debug(
            constants.CREATE_UPDATE_MSG, constants.UPADTING, Constants.CHAT, chat_data
        )
        chat_serializer = ChatDataSerializer(chat_instance, data=chat_data)
    else:
        # To create a new record
        logger.debug(
            constants.CREATE_UPDATE_MSG, constants.CREATING, Constants.CHAT, chat_data
        )
        chat_serializer = ChatDataSerializer(data=chat_data)
    if chat_serializer.is_valid():
        chat_serializer.save()
        logger.debug(constants.DATA_SAVED, Constants.CHAT)
        return True
    logger.debug(constants.INVALID_MSG, Constants.CHAT)
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
        chat_id=chat_data.get(Constants.ID), user_id=user_data_inst
    )
    user_chat_record.save()
    logger.debug(constants.DATA_SAVED, constants.USER_CHAT)
    return True
