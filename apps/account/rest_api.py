from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.account.utils import MospolytechParser
from apps.telegram.serializers import TelegramUserSerializer
from .models import MospolytechUser
from .serializers import MospolytechUserSerializer
from ..telegram.models import TelegramUser


class MospolytechUserViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    queryset = MospolytechUser.objects.all()
    serializer_class = MospolytechUserSerializer

    @action(detail=False, methods=['POST'], url_path='login-to-mospolytech')
    def login_to_mospolytech(self, request, *args, **kwargs):
        login = request.data.get('login')
        password = request.data.get('password')
        telegram = request.data.get('telegram')

        token = MospolytechParser.authenticate_mospolytech(login=login, password=password)

        serializer = TelegramUserSerializer(
            instance=TelegramUser.objects.get_or_none(telegram_id=telegram['telegram_id']), data=telegram)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user, _ = MospolytechUser.objects.update_or_create(login=login, defaults={'password': password,
                                                                                  'telegram_user': serializer.instance,
                                                                                  'cached_token': token})

        return Response(MospolytechUserSerializer(user).data, status=201)

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
