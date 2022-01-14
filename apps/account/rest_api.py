from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.account.utils import MospolytechParser
from apps.telegram.serializers import TelegramUserSerializer
from .models import MospolytechUser
from .serializers import MospolytechUserSerializer
from apps.telegram.models import TelegramUser

from rest_framework.exceptions import ValidationError


class MospolytechUserViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    queryset = MospolytechUser.objects.all()
    serializer_class = MospolytechUserSerializer

    @action(detail=False, methods=['POST'], url_path='login-to-mospolytech')
    def login_to_mospolytech(self, request, *args, **kwargs):
        login = request.data.get('login')
        password = request.data.get('password')
        telegram_id = request.data.get('telegram_id')

        if not (login or password or telegram_id):
            raise ValidationError(detail='Login, password and telegram_id would be passed')

        token = MospolytechParser.authenticate_mospolytech(login=login, password=password)

        user, created = MospolytechUser.objects.update_or_create(telegram_user__id=telegram_id, defaults={
            'login': login,
            'password': password,
            'cached_token': token})

        return Response(MospolytechUserSerializer(user).data, status=201 if created else 200)

    @action(detail=True, methods=['GET'], url_path='schedule')
    def schedule(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user.schedule, status=200)

    @action(detail=True, methods=['GET'], url_path='information')
    def information(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user.information, status=200)

    @action(detail=True, methods=['GET'], url_path='payments')
    def payments(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user.payments, status=200)
