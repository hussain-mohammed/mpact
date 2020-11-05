from rest_framework import serializers

from .models import ChatData, UserChat, UserData


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        #   fields = ['user_id','is_bot','first_name','last_name', 'language_code']
        exclude = ["joined_date"]


class ChatDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatData
        fields = "__all__"


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = "__all__"
