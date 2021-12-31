from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.utils import authenticate_mospolytech
from .models import MospolytechUser
from .serializers import MospolytechUserSerializer


class LoginToMospolytech(APIView):
    def post(self, request, *args, **kwargs):
        login = request.data.get('login')
        password = request.data.get('password')
        telegram_id = request.data.get('telegram_id')

        if not (login or password or telegram_id):
            raise ValidationError({'message': 'The request body must contain login, password, telegram_id'})

        authenticate_mospolytech(login=login, password=password)

        user, created = MospolytechUser.objects.update_or_create(login=login, password=password,
                                                                 telegram_id=telegram_id)

        serializer = MospolytechUserSerializer(user)
        status_code = 201 if created else 200

        return Response(serializer.data, status=status_code)
