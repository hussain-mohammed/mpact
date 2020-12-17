from rest_framework import serializers
from .models import ChatData


class ChatDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatData
        fields = "__all__"
