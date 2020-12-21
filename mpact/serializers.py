from rest_framework import serializers

from .models import Bot, Chat, Individual


class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = ["individual_id", "username", "first_name", "last_name"]


class BotSerializer(serializers.ModelSerializer):
    individuals = IndividualSerializer(many=True, required=True)

    class Meta:
        model = Bot
        fields = ["username", "individuals"]


class ChatSerializer(serializers.ModelSerializer):
    bot = BotSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ["chat_id", "title", "bot"]
