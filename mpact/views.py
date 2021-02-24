import asyncio

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from telegram_bot.constants import DATA, STATUS

from mpact.services import (
    create_flagged_message,
    delete_flagged_message,
    download_schedule_messages_file,
    get_dialog,
    get_flagged_messages,
    get_messages,
    schedule_messages,
    send_msg,
)


def new_or_current_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


class SendMessage(APIView):
    """
    This is a sample api to send a message.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        result = new_or_current_event_loop().run_until_complete(send_msg(data))
        return Response(result[DATA], status=result[STATUS])


class GetMessages(APIView):
    """
    returns the messages.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, room_id):
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        result = new_or_current_event_loop().run_until_complete(
            get_messages(room_id, limit, offset)
        )
        return Response(result[DATA], status=result[STATUS])


class Dialog(APIView):
    """
    It is used to retrive dialogs(open conversations)
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        result = new_or_current_event_loop().run_until_complete(get_dialog())
        return Response(result[DATA], status=result[STATUS])


class FlagMessage(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        result = new_or_current_event_loop().run_until_complete(
            get_flagged_messages(limit, offset)
        )
        return Response(result[DATA], status=result[STATUS])

    def post(self, request):
        data = request.data
        result = new_or_current_event_loop().run_until_complete(
            create_flagged_message(data)
        )
        return Response(result[DATA], status=result[STATUS])


class FlagMessageDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, id):
        result = new_or_current_event_loop().run_until_complete(
            delete_flagged_message(id)
        )
        return Response(result[DATA], status=result[STATUS])


class ScheduleMessages(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        result = new_or_current_event_loop().run_until_complete(
            download_schedule_messages_file()
        )
        return Response(result[DATA], status=result[STATUS])

    def post(self, request):
        file = request.data["file"]
        result = new_or_current_event_loop().run_until_complete(schedule_messages(file))
        return Response(result[DATA], status=result[STATUS])
