import asyncio

from constants import DATA, STATUS
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import (
    get_chat_msg,
    get_dialog,
    get_individual_msg,
    login,
    logout,
    send_msg,
)


def new_or_current_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


class Login(APIView):
    """
    It is used to login into telegram
    """

    def post(self, request):
        # request.data will contain phone or code.
        data = request.data
        result = new_or_current_event_loop().run_until_complete(login(data))
        return Response(result[DATA], status=result[STATUS])


class Logout(APIView):
    """
    It is used to log out from telegram.
    """

    def get(self, request):
        result = new_or_current_event_loop().run_until_complete(logout())
        return Response(result[DATA], status=result[STATUS])


class SendMessage(APIView):
    """
    This is a sample api to send a message.
    """

    def post(self, request):
        data = request.data
        result = new_or_current_event_loop().run_until_complete(send_msg(data))
        return Response(result[DATA], status=result[STATUS])


class GetIndividaulMessage(APIView):
    """
    returns the individual messages.
    """

    def get(self, request, individual_id):
        result = new_or_current_event_loop().run_until_complete(
            get_individual_msg(individual_id)
        )
        return Response(result[DATA], status=result[STATUS])


class GetChatMessage(APIView):
    """
    returns the chat messages.
    """

    def get(self, request, chat_id):
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        result = new_or_current_event_loop().run_until_complete(
            get_chat_msg(chat_id, limit, offset)
        )
        return Response(result[DATA], status=result[STATUS])


class Dialog(APIView):
    """
    It is used to retrive dialogs(open conversations)
    """

    def get(self, request):
        result = new_or_current_event_loop().run_until_complete(get_dialog())
        return Response(result[DATA], status=result[STATUS])
