import asyncio

from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import DATA, STATUS
from .services import get_dialog, login, logout, send_msg


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


class Dialog(APIView):
    """
    It is used to retrive dialogs(open conversations)
    """

    def get(self, request):
        result = new_or_current_event_loop().run_until_complete(get_dialog())
        return Response(result[DATA], status=result[STATUS])
