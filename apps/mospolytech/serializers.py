from rest_framework import serializers

from .models import MospolytechUser


class MospolytechUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    patronymic = serializers.CharField(required=False)

    class Meta:
        model = MospolytechUser
        fields = ['id', 'login', 'password', 'cached_token', 'telegram', 'name', 'surname', 'patronymic']
        extra_kwargs = {
            'password': {'write_only': True},
            'cached_token': {'write_only': True}
        }
