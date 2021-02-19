from django.urls import path

from .views import (
    Dialog,
    FlagMessage,
    FlagMessageDelete,
    GetChatMessage,
    GetIndividaulMessage,
    Login,
    Logout,
    ScheduleMessages,
    SendMessage,
)

urlpatterns = [
    path("login", Login.as_view()),
    path("logout", Logout.as_view()),
    path("message", SendMessage.as_view()),
    path("message/individual/<int:individual_id>", GetIndividaulMessage.as_view()),
    path("message/chat/<int:chat_id>", GetChatMessage.as_view()),
    path("dialogs", Dialog.as_view()),
    path("flaggedmessages", FlagMessage.as_view()),
    path("flaggedmessages/<int:id>", FlagMessageDelete.as_view()),
    path("schedule_messages", ScheduleMessages.as_view()),
]
