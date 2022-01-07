from rest_framework import serializers

from .models import MospolytechUser


class MospolytechUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MospolytechUser
        fields = ['id', 'login', 'telegram_user']
