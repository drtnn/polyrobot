from rest_framework import serializers

from .models import Lesson, ScheduledLesson, LessonPlace


class LessonPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlace
        fields = ['id', 'title', 'link']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'type', 'places', 'teachers']


class ScheduledLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledLesson
        fields = ['id', 'lesson', 'datetime']
