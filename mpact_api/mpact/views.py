import os

from rest_framework.response import Response
from rest_framework.views import APIView

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
        message = request.data["message"]
        chat_data = message.get("chat")
        from_data = message.get("from")

        if "new_chat_participant" in message:
            # This is used whenever bot or some other members are added to the group
            user_data = message.get("new_chat_participant")
            username = user_data.get("username")

            if username == os.environ.get("BOT_USERNAME"):
                # when our bot is added to the group. Bot will be saved to the Chat Data Model
                return Response(save_chatdata(chat_data))
            else:
                # when other member is added to the group. Member will be saved to the User Data Model and UserChat table for mapping.
                user_data_inst = save_userdata(user_data)
                if user_data_inst:
                    # Mapping between user and group is saved in UserChat Model
                    return Response(save_userchat(chat_data, user_data_inst))

        elif "new_chat_title" in message:
            # This is used whenever group title is changed.
            chat_instance = ChatData.objects.get(pk=chat_data.get("id"))
            return Response(save_chatdata(chat_data, chat_instance))

        elif "text" in message:
            # This is used whenever someone messages in the group.
            # It is used to store the existing user's details to UserData and UserChat Models
            try:
                user_instance = UserData.objects.get(pk=from_data.get("id"))
                user_chat_instance = UserChat.objects.get(
                    chat_id=chat_data.get("id"), user_id__id=from_data.get("id")
                )
            except (UserData.DoesNotExist, UserChat.DoesNotExist):
                user_serializer = UserDataSerializer(data=from_data)
                if user_serializer.is_valid():
                    # Storing user details in both UserData and UserChat Model
                    user_data_rec = UserData.objects.create(**from_data)
                    user_data_rec.save()
                    return Response(save_userchat(chat_data, user_data_rec))
                elif user_serializer.errors.get("id"):
                    # User already exists in user data model but does not exist in userchat model
                    return Response(save_userchat(chat_data, user_instance))

            # If user already exists in both the Models then just updating the details(firstname, lastname) in User Data Model
            user_serializer = UserDataSerializer(user_instance, data=from_data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response("ok")
        return Response("ok")
