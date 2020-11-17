from rest_framework import serializers

from .models import ChatData, UserChat, UserData


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        exclude = ["joined_date"]


class ChatDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatData
        fields = "__all__"
