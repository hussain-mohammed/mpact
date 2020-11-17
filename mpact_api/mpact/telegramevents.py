from .constants import (
    BOT_USERNAME,
    CHAT,
    FROM,
    ID,
    LEFT_CHAT_PARTICIPANT,
    NEW_CHAT_PARTICIPANT,
    USERNAME,
)
from .models import ChatData, UserChat, UserData
from .serializers import UserDataSerializer
from .services import save_chatdata, save_userchat


class TelegramEvents:
    def __init__(self, message):
        self.message = message
        self.chat_data = self.message[CHAT]
        self.from_data = self.message[FROM]

    def new_chat_participant(self):
        # This is used whenever bot or some other members are added to the group
        user_data = self.message[NEW_CHAT_PARTICIPANT]
        username = user_data.get(USERNAME)

        if username == BOT_USERNAME:
            # when our bot is added to the group. Bot will be saved to the Chat Data Model
            save_chatdata(self.chat_data)
        else:
            # when other member is added to the group. Member will be saved to the
            # User Data Model and UserChat table for mapping.
            try:
                user_instance = UserData.objects.get(pk=user_data[ID])
                user_chat_instance = UserChat.objects.get(
                    chat_id=self.chat_data[ID],
                    user__id=user_data[ID],
                )
            except UserData.DoesNotExist:
                add_user_chat_(user_data, self.chat_data)
                return True
            except (UserChat.DoesNotExist):
                add_user_chat_(user_data, self.chat_data, user_instance)
                return True
            # If member is added back to the same group, just change "is_deleted" to False
            user_chat_instance.is_deleted = False
            user_chat_instance.save()

    def new_chat_title(self):
        # This is used whenever group title is changed.
        chat_instance = ChatData.objects.get(pk=self.chat_data[ID])
        save_chatdata(self.chat_data, chat_instance)

    def text(self):
        # This is used whenever someone messages in the group.
        # It is used to store the existing user's details to UserData and UserChat Models
        try:
            user_instance = UserData.objects.get(pk=self.from_data[ID])
            user_chat_instance = UserChat.objects.get(
                chat_id=self.chat_data[ID],
                user__id=self.from_data[ID],
            )
        except UserData.DoesNotExist:
            add_user_chat_(self.from_data, self.chat_data)
            return True
        except (UserChat.DoesNotExist):
            add_user_chat_(self.from_data, self.chat_data, user_instance)
            return True

        # If user already exists in both the Models then just updating the
        # details(firstname, lastname) in User Data Model
        user_serializer = UserDataSerializer(user_instance, data=self.from_data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()

    def left_chat_participant(self):
        # When a member leaves a chat, it makes a safe delete.
        left_user_data = self.message[LEFT_CHAT_PARTICIPANT]
        try:
            user_chat_instance = UserChat.objects.get(
                chat_id=self.chat_data[ID],
                user__id=left_user_data[ID],
            )
        except UserChat.DoesNotExist as val_error:
            raise val_error
        user_chat_instance.is_deleted = True
        user_chat_instance.save()


def add_user_chat_(user_data, chat_data, user_instance=None):
    user_serializer = UserDataSerializer(data=user_data)
    if user_serializer.is_valid():
        # Storing user details in both UserData and UserChat Model
        user_data_rec = UserData.objects.create(**user_data)
        user_data_rec.save()
        save_userchat(chat_data, user_data_rec)
    elif user_serializer.errors[ID]:
        # User already exists in user data model but does not exist in userchat model
        save_userchat(chat_data, user_instance)
