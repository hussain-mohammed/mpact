from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import CustomUser


def validate_phone(username):
    if username[0] != "+":
        raise serializers.ValidationError("Phone number should start with '+'.")
    return username


class RegisterSerializer(serializers.ModelSerializer):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number is invalid.",
    )
    phone = serializers.CharField(validators=[phone_regex, validate_phone])
    password = serializers.CharField(write_only=True)
    email = None

    class Meta:
        model = CustomUser
        fields = ["phone", "first_name", "last_name", "password"]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
