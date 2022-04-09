from rest_framework import serializers

from .models import UserPreference


class UserPreferenceSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(source='preference.slug')
    max_value = serializers.IntegerField(source='preference.max_value')

    class Meta:
        model = UserPreference
        fields = ['id', 'slug', 'enabled', 'value', 'max_value']
