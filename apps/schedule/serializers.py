from rest_framework import serializers

from apps.s3.serializers import FileSerializer
from .models import Lesson, ScheduledLesson, LessonPlace, LessonRoom, LessonTeacher, LessonType, ScheduledLessonNote
from apps.s3.models import File


class LessonRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonRoom
        fields = ['id', 'number']


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
        fields = ['id', 'lesson', 'datetime', 'text', 'files']


class ScheduledLessonNoteWriteSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(many=True, queryset=File.objects.all(), required=False)

    class Meta:
        model = ScheduledLessonNote
        fields = ['id', 'lesson', 'datetime', 'text', 'files']


class ScheduledLessonAddNoteSerializer(serializers.ModelSerializer):
    scheduled_lesson = serializers.PrimaryKeyRelatedField(queryset=ScheduledLesson.objects.all())
    files = serializers.PrimaryKeyRelatedField(many=True, queryset=File.objects.all(), required=False)

    class Meta:
        model = ScheduledLessonNote
        fields = ['scheduled_lesson', 'text', 'files']

    def create(self, validated_data):
        scheduled_lesson = validated_data.pop('scheduled_lesson')
        validated_data['lesson'], validated_data['datetime'] = scheduled_lesson.lesson, scheduled_lesson.datetime
        return super(ScheduledLessonAddNoteSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('scheduled_lesson'):
            scheduled_lesson = validated_data.pop('scheduled_lesson')
            validated_data['lesson'], validated_data['datetime'] = scheduled_lesson.lesson, scheduled_lesson.datetime
        return super(ScheduledLessonAddNoteSerializer, self).update(instance=instance, validated_data=validated_data)
