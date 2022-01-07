from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.utils import MospolytechParser
from apps.telegram.serializers import TelegramUserSerializer
from .models import MospolytechUser
from .serializers import MospolytechUserSerializer
from ..telegram.models import TelegramUser


class LoginToMospolytech(APIView):
    def post(self, request, *args, **kwargs):
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
