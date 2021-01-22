import asyncio

from constants import DATA, STATUS
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import token_required

from mpact.services import (
    get_chat_msg,
    get_dialog,
    get_individual_msg,
    login,
    logout,
    send_msg,
)
from rest_framework import status
from mpact.serializers import FlaggedMessageSerializer
from mpact.models import FlaggedMessage
from constants import (
    IS_SUCCESS,
    MESSAGE,
    RECORD_NF,
    DELETE_SUCCESS,
    DELETE_FAIL,
    FLAGGED_MESSAGE,
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

    @token_required
    def get(self, request, phone):
        result = new_or_current_event_loop().run_until_complete(logout(phone))
        return Response(result[DATA], status=result[STATUS])


class SendMessage(APIView):
    """
    This is a sample api to send a message.
    """

    @token_required
    def post(self, request, phone):
        data = request.data
        result = new_or_current_event_loop().run_until_complete(send_msg(phone, data))
        return Response(result[DATA], status=result[STATUS])


class GetIndividaulMessage(APIView):
    """
    returns the individual messages.
    """

    @token_required
    def get(self, request, phone, individual_id):
        result = new_or_current_event_loop().run_until_complete(
            get_individual_msg(phone, individual_id)
        )
        return Response(result[DATA], status=result[STATUS])


class GetChatMessage(APIView):
    """
    returns the chat messages.
    """

    @token_required
    def get(self, request, phone, chat_id):
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        result = new_or_current_event_loop().run_until_complete(
            get_chat_msg(phone, chat_id, limit, offset)
        )
        return Response(result[DATA], status=result[STATUS])


class Dialog(APIView):
    """
    It is used to retrive dialogs(open conversations)
    """

    @token_required
    def get(self, request, phone):
        result = new_or_current_event_loop().run_until_complete(get_dialog(phone))
        return Response(result[DATA], status=result[STATUS])


class FlagMessage(APIView):
    @token_required
    def get(self, request, phone):
        queryset = FlaggedMessage.objects.all()
        serializer = FlaggedMessageSerializer(queryset, many=True)
        return Response(
            {FLAGGED_MESSAGE: serializer.data, IS_SUCCESS: True},
            status=status.HTTP_200_OK,
        )

    @token_required
    def post(self, request, phone):
        data = request.data
        serializer = FlaggedMessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {FLAGGED_MESSAGE: serializer.data, IS_SUCCESS: True},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {MESSAGE: serializer.errors, IS_SUCCESS: False},
                status=status.HTTP_400_BAD_REQUEST,
            )


class FlagMessageDelete(APIView):
    @token_required
    def delete(self, request, phone, id):
        try:
            flagged_message = FlaggedMessage.objects.get(pk=id)
        except FlaggedMessage.DoesNotExist:
            return Response(
                {MESSAGE: RECORD_NF, IS_SUCCESS: False},
                status=status.HTTP_404_NOT_FOUND,
            )

        if flagged_message.delete():
            return Response(
                {MESSAGE: DELETE_SUCCESS, IS_SUCCESS: True}, status=status.HTTP_200_OK
            )
        return Response(
            {MESSAGE: DELETE_FAIL, IS_SUCCESS: False},
            status=status.HTTP_400_BAD_REQUEST,
        )
