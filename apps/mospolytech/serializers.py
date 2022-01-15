from rest_framework import serializers

from .models import MospolytechUser, PersonalData


class MospolytechUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MospolytechUser
        fields = ['id', 'login', 'password', 'cached_token', 'telegram']
        extra_kwargs = {
            'password': {'write_only': True},
            'cached_token': {'write_only': True}
        }
