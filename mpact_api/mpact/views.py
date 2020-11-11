from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from . import constants
from .logger import logger
from .services import set_webhook
from .telegramevents import TelegramEvents


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
        """
        Sample ``request.data``::
        {
            "update_id": 30927953,
            "message": {
                "message_id": 51,
                "from": {
                    "id": 1229986355,
                    "is_bot": False,
                    "first_name": "John",
                    "last_name": "Walter",
                    "language_code": "en"
                },
                "chat": {
                    "id": -433354696,
                    "title": "Testing Group",
                    "type": "group",
                    "all_members_are_administrators": True
                },
                "date": 1604317469,

                /** Someone sends a message in a group: */
                "text": "Hello, How are you?"

                /** Someone joins a chat: */
                "new_chat_participant": {
                    "id": 1321604047,
                    "is_bot": True,
                    "first_name": "demo_bot",
                    "username": "test_bot"
                },
                "new_chat_member": {
                    "id": 1321604047,
                    "is_bot": True,
                    "first_name": "demo_bot",
                    "username": "test_bot"
                },
                "new_chat_members": [
                    {
                            "id": 1321604047,
                            "is_bot": True,
                            "first_name": "demo_bot",
                            "username": "test_bot"
                    }
                ]

                /** Someone leaves a chat: */
                "left_chat_member": {
                    "id": 879250491,
                    "is_bot": False,
                    "first_name": "John",
                    "last_name": "Walter"
                }
            }
        }
        """
        try:
            message = request.data.get(constants.MESSAGE)
            event = TelegramEvents(message)
            # TELEGRAM_EVENTS is a set of event names :: {
            # "new_chat_participant",
            # "new_chat_title",
            # "text",
            # }
            # Here taking out the common event between set and incoming request_data
            # and calling the method from TELEGRAM_EVENTS class
            getattr(event, list(constants.TELEGRAM_EVENTS.intersection(message))[0])()

        except IndexError as index_error:
            logger.exception(index_error)
        except AttributeError as attribute_error:
            logger.exception(attribute_error)
        except serializers.ValidationError as validation_error:
            logger.exception(validation_error)
        except Exception as e:
            logger.exception(e)

        return Response(constants.OK)
