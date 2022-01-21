from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.mospolytech.utils import MospolytechParser
from .models import MospolytechUser
from .serializers import MospolytechUserSerializer
from ..schedule.serializers import ScheduledLessonReadSerializer


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

        if not (login or password or telegram):
            raise ValidationError(detail='Login, password and telegram_id must be passed')

        token = MospolytechParser.authenticate_mospolytech(login=login, password=password)

        user = MospolytechUser.objects.get_or_none(telegram=telegram)
        serializer = MospolytechUserSerializer(instance=user, data=request.data | {'cached_token': token})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

    @action(detail=True, methods=['GET'], url_path='schedule')
    def schedule(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user.schedule(is_session=False), status=200)

    @action(detail=True, methods=['GET'], url_path='session-schedule')
    def session_schedule(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user.schedule(is_session=True), status=200)

    @action(detail=True, methods=['GET'], url_path='information')
    def information(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user.information(), status=200)

    @action(detail=True, methods=['GET'], url_path='payments')
    def payments(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user.payments(), status=200)

    @action(detail=True, methods=['GET'], url_path='academic-performance')
    def academic_performance(self, request, *args, **kwargs):
        user = self.get_object()
        semester_number = request.query_params.get('semester_number', None)
        semester_number = semester_number[0] if isinstance(semester_number, list) else semester_number

        return Response(user.academic_performance(semester_number=semester_number), status=200)

    @action(detail=True, methods=['GET'], url_path='scheduled-lessons')
    def scheduled_lessons(self, request, *args, **kwargs):
        user = self.get_object()
        date = request.query_params.get('date', None)
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)

        scheduled_lessons = user.scheduled_lessons
        if date:
            scheduled_lessons = user.scheduled_lessons.filter(datetime__contains=date)
        else:
            if date_from:
                scheduled_lessons = user.scheduled_lessons.filter(datetime__gte=date_from)
            if date_to:
                scheduled_lessons = user.scheduled_lessons.filter(datetime__lte=date_to)
        serializer = ScheduledLessonReadSerializer(scheduled_lessons, many=True)

        return Response(serializer.data, status=200)
