from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


def validate_phone(username):
    if username[0] != "+":
        raise ValidationError("Phone number should start with '+'.")
    return username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number is invalid.",
    )
    phone = models.CharField(max_length=20, validators=[phone_regex, validate_phone])


class Chat(models.Model):
    chat_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=350)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.chat_id} - {self.title}"


class Bot(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE)
    bot_id = models.IntegerField()
    username = models.CharField(max_length=350)
    first_name = models.CharField(max_length=350)
    last_name = models.CharField(max_length=350, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["chat", "bot_id"], name="unique_chat_bot")
        ]

    def __str__(self):
        return f"{self.bot_id} - {self.username}"


class Individual(models.Model):
    bot = models.ForeignKey(Bot, related_name="individuals", on_delete=models.CASCADE)
    individual_id = models.IntegerField()
    username = models.CharField(max_length=350, null=True)
    first_name = models.CharField(max_length=350)
    last_name = models.CharField(max_length=350)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["bot", "individual_id"], name="unique_bot_individuals"
            )
        ]

    def __str__(self):
        return f"{self.individual_id} - {self.first_name}"
