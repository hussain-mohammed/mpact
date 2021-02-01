from rest_framework import serializers

from .models import (
    Bot,
    BotIndividual,
    Chat,
    ChatBot,
    Individual,
    Message,
    FlaggedMessage,
)


class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        exclude = ["access_hash", "bots"]


class BotIndividualSerializer(serializers.ModelSerializer):
    individual = IndividualSerializer(required=True, many=False)

    class Meta:
        model = BotIndividual
        fields = ["individual"]


class BotSerializer(serializers.ModelSerializer):
    bot_individuals = BotIndividualSerializer(required=True, many=True)

    class Meta:
        model = Bot
        fields = ["id", "username", "bot_individuals"]


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "title"]


class ChatBotSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(read_only=True)
    bot = BotSerializer(read_only=True)

    class Meta:
        model = ChatBot
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "individual", "sender", "message", "date"]
        read_only_fields = ["id", "date"]


class FlaggedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlaggedMessage
        fields = ["id", "room_id", "message_id", "first_name", "message", "date"]
        read_only_fields = ["id", "date"]
