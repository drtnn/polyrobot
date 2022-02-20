from rest_framework import serializers

from apps.s3.models import File
from apps.s3.serializers import FileSerializer
from .models import Lesson, ScheduledLesson, LessonPlace, LessonRoom, LessonTeacher, LessonType, ScheduledLessonNote


class LessonRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonRoom
        fields = ['number']


class LessonPlaceSerializer(serializers.ModelSerializer):
    rooms = LessonRoomSerializer(many=True)

    class Meta:
        model = LessonPlace
        fields = ['title', 'link', 'rooms']


class LessonTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTeacher
        fields = ['full_name']


class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = ['title']


class LessonReadSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.number')
    type = serializers.CharField(source='type.title')
    place = LessonPlaceSerializer()
    teachers = LessonTeacherSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['title', 'group', 'type', 'place', 'teachers']


class ScheduledLessonSerializer(serializers.ModelSerializer):
    lesson = LessonReadSerializer()

    class Meta:
        model = ScheduledLesson
        fields = ['id', 'lesson', 'datetime']


class ScheduledLessonNoteReadSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = ScheduledLessonNote
        fields = ['id', 'scheduled_lesson', 'text', 'files']


class ScheduledLessonNoteWriteSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(many=True, queryset=File.objects.all(), required=False)

    class Meta:
        model = ScheduledLessonNote
        fields = ['id', 'scheduled_lesson', 'text', 'files']

