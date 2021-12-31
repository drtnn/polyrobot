from rest_framework import serializers

from apps.account.models import MospolytechUser


class MospolytechUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MospolytechUser
        fields = ['login', 'telegram_id']
