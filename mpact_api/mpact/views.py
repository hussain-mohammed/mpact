import asyncio

from rest_framework.views import APIView

from .services import get_dialog, login, logout, send_msg, exception


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

    @exception
    def post(self, request):
        # request.data will contain phone or code.
        data = request.data
        return new_or_current_event_loop().run_until_complete(login(data))


class Logout(APIView):
    """
    It is used to log out from telegram.
    """

    @exception
    def get(self, request):
        return new_or_current_event_loop().run_until_complete(logout())


class SendMessage(APIView):
    """
    This is a sample api to send a message.
    """

    @exception
    def post(self, request):
        data = request.data
        return new_or_current_event_loop().run_until_complete(send_msg(data))


class Dialog(APIView):
    """
    It is used to retrive dialogs(open conversations)
    """

    @exception
    def get(self, request):
        return new_or_current_event_loop().run_until_complete(get_dialog())
