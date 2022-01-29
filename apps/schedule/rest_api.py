from datetime import datetime

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.mospolytech.models import Group
from apps.s3.models import File
from apps.schedule.models import ScheduledLesson, ScheduledLessonNote
from apps.schedule.serializers import ScheduledLessonSerializer, ScheduledLessonNoteReadSerializer, \
    ScheduledLessonNoteWriteSerializer


class ScheduledLessonViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = ScheduledLessonSerializer
    queryset = ScheduledLesson.objects.all().order_by('datetime')

    def get_queryset(self):
        qs = self.queryset
        date = self.request.query_params.get('date', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if 'telegram_pk' in self.kwargs:
            group = Group.objects.get(student__user__telegram_id=self.kwargs['telegram_pk'])
            qs = qs.filter(lesson__group=group)

        date = datetime.today().date() if date == 'today' else date

        if date:
            qs = qs.filter(datetime__contains=date)
        else:
            if date_from:
                qs = qs.filter(datetime__gte=date_from)
            if date_to:
                qs = qs.filter(datetime__lte=date_to)
        return qs

    @action(detail=True, methods=['POST'], url_path='add-note')
    def add_note(self, request, *args, **kwargs):
        scheduled_lesson = self.get_object()

        serializer = ScheduledLessonNoteWriteSerializer(data=request.data | {'scheduled_lesson': scheduled_lesson.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)


class ScheduledLessonNoteViewSet(viewsets.ModelViewSet):
    queryset = ScheduledLessonNote.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'perform_update'):
            return ScheduledLessonNoteWriteSerializer
        return ScheduledLessonNoteReadSerializer

    def get_queryset(self):
        qs = self.queryset

        if 'scheduled_lesson_pk' in self.kwargs:
            qs = qs.filter(scheduled_lesson__id=self.kwargs['scheduled_lesson_pk'])
        return qs

    @action(detail=True, methods=['POST'], url_path='add-file')
    def add_note(self, request, *args, **kwargs):
        note = self.get_object()
        files = request.data.get('files')

        if not isinstance(files, list):
            raise ValidationError({'error': '`files` is not valid'})
        note.files.add(File.objects.filter(id__in=files))

        serializer = ScheduledLessonNoteReadSerializer(instance=note)
        return Response(serializer.data, status=200)
