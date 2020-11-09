from rest_framework.response import Response
from rest_framework.views import APIView

from . import constants
from .logger import logger
from .models import ChatData, UserChat, UserData
from .serializers import UserDataSerializer
from .services import save_chatdata, save_userchat, save_userdata, set_webhook


class Webhook(APIView):
    """
    This is only called once for the webhook setup.
    """

    def get(self, request):
        webhook = set_webhook()
        if webhook:
            return Response("webhook setup ok")
        else:
            return Response("webhook setup failed")


class ListenMessages(APIView):
    """
    Telegram webhook makes a post request.
    """

    def post(self, request):
        message = request.data.get(constants.MESSAGE)
        logger.debug(message)
        chat_data = message.get(constants.CHAT)
        from_data = message.get(constants.FROM)

        if constants.NEW_CHAT_PARTICIPANT in message:
            # This is used whenever bot or some other members are added to the group
            user_data = message.get(constants.NEW_CHAT_PARTICIPANT)
            username = user_data.get(constants.USERNAME)

            if username == constants.BOT_USERNAME:
                # when our bot is added to the group. Bot will be saved to the Chat Data Model
                return Response(save_chatdata(chat_data))
            else:
                # when other member is added to the group. Member will be saved to the User Data Model and UserChat table for mapping.
                user_data_inst = save_userdata(user_data)
                if user_data_inst:
                    # Mapping between user and group is saved in UserChat Model
                    return Response(save_userchat(chat_data, user_data_inst))

        elif constants.NEW_CHAT_TITLE in message:
            # This is used whenever group title is changed.
            chat_instance = ChatData.objects.get(pk=chat_data.get(constants.ID))
            return Response(save_chatdata(chat_data, chat_instance))

        elif constants.TEXT in message:
            # This is used whenever someone messages in the group.
            # It is used to store the existing user's details to UserData and UserChat Models
            try:
                user_instance = UserData.objects.get(pk=from_data.get(constants.ID))
                user_chat_instance = UserChat.objects.get(
                    chat_id=chat_data.get(constants.ID),
                    user_id__id=from_data.get(constants.ID),
                )
            except (UserData.DoesNotExist, UserChat.DoesNotExist):
                logger.debug(
                    constants.CREATE_UPDATE_MSG,
                    constants.CREATING,
                    constants.USER,
                    from_data,
                )
                user_serializer = UserDataSerializer(data=from_data)
                if user_serializer.is_valid():
                    # Storing user details in both UserData and UserChat Model
                    user_data_rec = UserData.objects.create(**from_data)
                    user_data_rec.save()
                    logger.debug(constants.DATA_SAVED, constants.USER)
                    return Response(save_userchat(chat_data, user_data_rec))
                elif user_serializer.errors.get(constants.ID):
                    # User already exists in user data model but does not exist in userchat model
                    return Response(save_userchat(chat_data, user_instance))

            # If user already exists in both the Models then just updating the details(firstname, lastname) in User Data Model
            logger.debug(
                constants.CREATE_UPDATE_MSG,
                constants.UPADTING,
                constants.USER,
                from_data,
            )
            user_serializer = UserDataSerializer(user_instance, data=from_data)
            if user_serializer.is_valid():
                user_serializer.save()
                logger.debug(constants.DATA_SAVED, constants.USER)
                return Response(constants.OK)

        logger.debug(constants.WEBHOOK_END)
        return Response(constants.OK)
