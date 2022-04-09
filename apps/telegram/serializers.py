from rest_framework import serializers

from apps.preference.serializers import UserPreferenceSerializer
from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    preferences = UserPreferenceSerializer(many=True)

    class Meta:
        model = TelegramUser
        fields = ['id', 'username', 'full_name', 'is_admin', 'preferences']
