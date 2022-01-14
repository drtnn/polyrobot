from rest_framework import viewsets

from apps.telegram.models import TelegramUser
from apps.telegram.serializers import TelegramUserSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()
