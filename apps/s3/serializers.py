from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'created_at', 'data']

    def validate_data(self, value):
        limit = 20 * 1024 * 1024
        if value.size > limit:
            raise ValidationError({'error': 'File is too large. Size should not exceed 20 MiB.'})
        return value
