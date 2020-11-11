from . import constants
from .models import ChatData, UserChat, UserData
from .serializers import UserDataSerializer
from .services import save_chatdata, save_userchat, save_userdata


class TelegramEvents:
    def __init__(self, message):
        self.message = message
        self.chat_data = self.message.get(constants.CHAT)
        self.from_data = self.message.get(constants.FROM)

    def new_chat_participant(self):
        # This is used whenever bot or some other members are added to the group
        user_data = self.message.get(constants.NEW_CHAT_PARTICIPANT)
        username = user_data.get(constants.USERNAME)

        if username == constants.BOT_USERNAME:
            # when our bot is added to the group. Bot will be saved to the Chat Data Model
            save_chatdata(self.chat_data)
        else:
            # when other member is added to the group. Member will be saved to the
            # User Data Model and UserChat table for mapping.
            user_data_inst = save_userdata(user_data)
            if user_data_inst:
                # Mapping between user and group is saved in UserChat Model
                save_userchat(self.chat_data, user_data_inst)

    def new_chat_title(self):
        # This is used whenever group title is changed.
        chat_instance = ChatData.objects.get(pk=self.chat_data.get(constants.ID))
        save_chatdata(self.chat_data, chat_instance)

    def text(self):
        # This is used whenever someone messages in the group.
        # It is used to store the existing user's details to UserData and UserChat Models
        try:
            user_instance = UserData.objects.get(pk=self.from_data.get(constants.ID))
            user_chat_instance = UserChat.objects.get(
                chat_id=self.chat_data.get(constants.ID),
                user_id__id=self.from_data.get(constants.ID),
            )
        except (UserData.DoesNotExist, UserChat.DoesNotExist):
            user_serializer = UserDataSerializer(data=self.from_data)
            if user_serializer.is_valid():
                # Storing user details in both UserData and UserChat Model
                user_data_rec = UserData.objects.create(**self.from_data)
                user_data_rec.save()
                save_userchat(self.chat_data, user_data_rec)
            elif user_serializer.errors.get(constants.ID):
                # User already exists in user data model but does not exist in userchat model
                save_userchat(self.chat_data, user_instance)
            return True

        # If user already exists in both the Models then just updating the
        # details(firstname, lastname) in User Data Model
        user_serializer = UserDataSerializer(user_instance, data=self.from_data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
