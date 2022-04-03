import logging

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from telebot.apihelper import ApiTelegramException

from apps.mospolytech.utils import MospolytechParser
from apps.telegram.bot import bot
from .models import MospolytechUser
from .serializers import MospolytechUserSerializer

logger = logging.getLogger(__name__)


class MospolytechUserViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    queryset = MospolytechUser.objects.all()
    serializer_class = MospolytechUserSerializer

    @action(detail=False, methods=['POST'], url_path='login-to-mospolytech', permission_classes=[AllowAny])
    def login_to_mospolytech(self, request, *args, **kwargs):
        login = request.data.get('login')
        password = request.data.get('password')
        telegram = request.data.get('telegram')

        if not (login and password and telegram):
            raise ValidationError({'error': 'login, password and telegram must be passed'})

        token = MospolytechParser.authenticate_mospolytech(login=login, password=password)

        user = MospolytechUser.objects.get_or_none(telegram=telegram)
        info = MospolytechParser.get_data_from_mospolytech_by_token(token=token, key=MospolytechParser.USER)['user']

        serializer = MospolytechUserSerializer(instance=user, data={
            'login': login,
            'password': password,
            'telegram': telegram,
            'cached_token': token,
            'name': info['name'],
            'surname': info['surname'],
            'patronymic': info['patronymic'],
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            bot.send_message(
                telegram, "🤖 Регистрация пройдена успешно, теперь тебе полностью доступен функционал бота."
            )
        except ApiTelegramException:
            logger.info('Can not send success registration message')

        return Response(serializer.data, status=200)
