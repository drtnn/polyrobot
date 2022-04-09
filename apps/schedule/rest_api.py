from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.mospolytech.models import Group
from apps.s3.models import File
from apps.schedule.models import ScheduledLesson, ScheduledLessonNote, ScheduledLessonNotification
from apps.schedule.serializers import ScheduledLessonSerializer, ScheduledLessonNoteReadSerializer, \
    ScheduledLessonNoteWriteSerializer, ScheduledLessonNotificationSerializer
from apps.schedule.utils import export_scheduled_lessons


class ScheduledLessonViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = ScheduledLessonSerializer
    queryset = ScheduledLesson.objects.all().order_by('datetime')

    def get_queryset(self):
        qs = self.queryset
        datetime = self.request.query_params.get('date', None)
        datetime_from = self.request.query_params.get('datetime_from', None)
        datetime_to = self.request.query_params.get('datetime_to', None)

        if 'telegram_pk' in self.kwargs:
            group = Group.objects.get(students__user__telegram_id=self.kwargs['telegram_pk'])
            qs = qs.filter(lesson__group=group)

        if datetime:
            qs = qs.filter(datetime__contains=datetime)
        else:
            if datetime_from:
                qs = qs.filter(datetime__gte=datetime_from)
            if datetime_to:
                qs = qs.filter(datetime__lte=datetime_to)
        return qs

    @action(detail=True, methods=['POST'], url_path='add-note')
    def add_note(self, request, *args, **kwargs):
        scheduled_lesson = self.get_object()

        serializer = ScheduledLessonNoteWriteSerializer(data=request.data | {'scheduled_lesson': scheduled_lesson.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(ScheduledLessonNoteReadSerializer(serializer.instance).data, status=200)

    @action(detail=False, methods=['GET'])
    def export(self, request, *args, **kwargs):
        filename = 'Расписание.ics'
        calendar = export_scheduled_lessons(self.get_queryset())

        response = HttpResponse(calendar, content_type='text/calendar')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class ScheduledLessonNoteViewSet(viewsets.ModelViewSet):
    queryset = ScheduledLessonNote.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'perform_update'):
            return ScheduledLessonNoteWriteSerializer
        return ScheduledLessonNoteReadSerializer

    def get_queryset(self):
        qs = self.queryset

        if 'scheduled_lesson_pk' in self.kwargs:
            scheduled_lesson = ScheduledLesson.objects.get_or_none(id=self.kwargs['scheduled_lesson_pk'])
            qs = qs.filter(scheduled_lesson=scheduled_lesson)
        return qs

    @action(detail=True, methods=['POST'], url_path='add-file')
    def add_file(self, request, *args, **kwargs):
        note = self.get_object()
        files = request.data.get('files')

        if not isinstance(files, list):
            raise ValidationError({'error': '`files` is not valid'})
        note.files.add(*File.objects.filter(id__in=files))

        return Response(ScheduledLessonNoteReadSerializer(instance=note).data, status=200)


class ScheduledLessonNotificationViewSet(mixins.ListModelMixin,
                                         mixins.RetrieveModelMixin,
                                         viewsets.GenericViewSet):
    serializer_class = ScheduledLessonNotificationSerializer
    queryset = ScheduledLessonNotification.objects.all().order_by('notify_at')

    def get_queryset(self):
        qs = self.queryset
        notify_from = self.request.query_params.get('notify_from', None)
        notify_to = self.request.query_params.get('notify_to', None)

        if 'scheduled_lesson_pk' in self.kwargs:
            scheduled_lesson = ScheduledLesson.objects.get_or_none(id=self.kwargs['scheduled_lesson_pk'])
            qs = qs.filter(scheduled_lesson=scheduled_lesson)

        if notify_from:
            qs = qs.filter(notify_at__gte=notify_from)
        if notify_to:
            qs = qs.filter(notify_at__lte=notify_to)
        return qs
