from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.telegram.models import TelegramUser
from apps.telegram.serializers import TelegramUserSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()

    @action(detail=True, methods=['GET'], url_path='schedule')
    def schedule(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()

        try:
            user = telegram_user.mospolytechuser
        except TelegramUser.mospolytechuser.RelatedObjectDoesNotExist:
            raise ValidationError({'error': 'TelegramUser is not logged in.'})

        return Response(user.schedule(is_session=False), status=200)

    @action(detail=True, methods=['GET'], url_path='session-schedule')
    def session_schedule(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()

        try:
            user = telegram_user.mospolytechuser
        except TelegramUser.mospolytechuser.RelatedObjectDoesNotExist:
            raise ValidationError({'error': 'TelegramUser is not logged in.'})

        return Response(user.schedule(is_session=True), status=200)

    @action(detail=True, methods=['GET'], url_path='profile')
    def profile(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()

        try:
            user = telegram_user.mospolytechuser
        except TelegramUser.mospolytechuser.RelatedObjectDoesNotExist:
            raise ValidationError({'error': 'TelegramUser is not logged in.'})

        return Response(user.profile(), status=200)

    @action(detail=True, methods=['GET'], url_path='payments')
    def payments(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()

        try:
            user = telegram_user.mospolytechuser
        except TelegramUser.mospolytechuser.RelatedObjectDoesNotExist:
            raise ValidationError({'error': 'TelegramUser is not logged in.'})

        return Response(user.payments(), status=200)

    @action(detail=True, methods=['GET'], url_path='academic-performance')
    def academic_performance(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()

        try:
            user = telegram_user.mospolytechuser
        except TelegramUser.mospolytechuser.RelatedObjectDoesNotExist:
            raise ValidationError({'error': 'TelegramUser is not logged in.'})

        semester_number = request.query_params.get('semester_number', None)
        semester_number = semester_number[0] if isinstance(semester_number, list) else semester_number

        return Response(user.academic_performance(semester_number=semester_number), status=200)
