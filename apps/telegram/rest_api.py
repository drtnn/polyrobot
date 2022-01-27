from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.telegram.models import TelegramUser
from apps.telegram.serializers import TelegramUserSerializer
from apps.schedule.serializers import ScheduledLessonSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()

    @action(detail=True, methods=['GET'], url_path='schedule')
    def schedule(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()
        user = telegram_user.mospolytechuser

        return Response(user.schedule(is_session=False), status=200)

    @action(detail=True, methods=['GET'], url_path='session-schedule')
    def session_schedule(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()
        user = telegram_user.mospolytechuser

        return Response(user.schedule(is_session=True), status=200)

    @action(detail=True, methods=['GET'], url_path='information')
    def information(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()
        user = telegram_user.mospolytechuser

        return Response(user.information(), status=200)

    @action(detail=True, methods=['GET'], url_path='payments')
    def payments(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()
        user = telegram_user.mospolytechuser

        return Response(user.payments(), status=200)

    @action(detail=True, methods=['GET'], url_path='academic-performance')
    def academic_performance(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()
        user = telegram_user.mospolytechuser

        semester_number = request.query_params.get('semester_number', None)
        semester_number = semester_number[0] if isinstance(semester_number, list) else semester_number

        return Response(user.academic_performance(semester_number=semester_number), status=200)

    @action(detail=True, methods=['GET'], url_path='scheduled-lessons')
    def scheduled_lessons(self, request, *args, **kwargs):
        telegram_user: TelegramUser = self.get_object()
        user = telegram_user.mospolytechuser

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
        serializer = ScheduledLessonSerializer(scheduled_lessons, many=True)

        return Response(serializer.data, status=200)
