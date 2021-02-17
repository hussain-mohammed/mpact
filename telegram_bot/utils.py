from itsdangerous import URLSafeSerializer
from telegram_bot.constants import (
    SECURED_URL_SECRET_KEY,
    SECURITY_PASSWORD_SALT,
    PHONE,
    NOT_AUTHORIZED,
    DATA,
    MESSAGE,
)
from rest_framework.response import Response
from telegram_bot.logger import logger


def get_or_none(model, **kwargs):
    """
    Returns model object if exists else None
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def encode_token(token):
    # TODO: Instead of creating a separate `SECURED_URL_SECRET_KEY`
    #       constant, just reuse `settings.SECRET_KEY`.
    serializer = URLSafeSerializer(SECURED_URL_SECRET_KEY)

    # TODO: `salt` is optional, and does not need to be secret. It's
    #       used as a namespace.
    #       See https://itsdangerous.palletsprojects.com/en/1.1.x/serializer/#the-salt
    encoded_token = serializer.dumps(token, salt=SECURITY_PASSWORD_SALT)
    return encoded_token


def decode_token(token):
    serializer = URLSafeSerializer(SECURED_URL_SECRET_KEY)
    user_id = serializer.loads(token, salt=SECURITY_PASSWORD_SALT)
    return user_id


def token_required(func):
    def wrapper(*args, **kwargs):
        try:
            request = args[1]
            token = request.headers["token"]
            phone = decode_token(token)[PHONE]
        except KeyError as key_error:
            logger.exception(key_error)
            NOT_AUTHORIZED[DATA][MESSAGE] = "TOKEN is required"
            return Response(NOT_AUTHORIZED[DATA], 401)

        except Exception as exception:
            logger.exception(exception)
            NOT_AUTHORIZED[DATA][MESSAGE] = "TOKEN is invalid"
            return Response(NOT_AUTHORIZED[DATA], 401)
        return func(*args, phone=phone, **kwargs)

    return wrapper
