from datetime import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class UserData(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    is_bot = models.BooleanField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    joined_date = models.DateTimeField(default=timezone.now)
    language_code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f" {self.id} - {self.first_name}"


class ChatData(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=160)
    type = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True)
    all_members_are_administrators = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f" {self.title} - {self.type}"


class UserChat(models.Model):
    chat_id = models.CharField(max_length=50)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)

    def __str__(self):
        return f"chat_id: {self.chat_id}, user: {self.user}"
