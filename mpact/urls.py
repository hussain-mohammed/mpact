from django.urls import path

from .views import (
    Dialog,
    ExportMessages,
    FlagMessage,
    FlagMessageDelete,
    GetMessages,
    ScheduleMessages,
    SendMessage,
)

urlpatterns = [
    path("messages", SendMessage.as_view()),
    path("messages/<int:room_id>", GetMessages.as_view()),
    path("dialogs", Dialog.as_view()),
    path("flaggedmessages", FlagMessage.as_view()),
    path("flaggedmessages/<int:id>", FlagMessageDelete.as_view()),
    path("schedule_messages", ScheduleMessages.as_view()),
    path("export_messages", ExportMessages.as_view()),
]
