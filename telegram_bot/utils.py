from rest_framework import status

from telegram_bot.constants import DATA, FAIL_MSG, IS_SUCCESS, MESSAGE, STATUS
from telegram_bot.logger import logger


def get_or_none(model, **kwargs):
    """
    Returns model object if exists else None
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def exception(function):
    async def wrapper(*args):
        try:
            func = await function(*args)
            return func
        except Exception as exception:
            logger.exception(exception)
            return {
                DATA: {MESSAGE: FAIL_MSG, IS_SUCCESS: False},
                STATUS: status.HTTP_400_BAD_REQUEST,
            }

    return wrapper
