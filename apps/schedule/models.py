from django.db import models

from apps.core.models import BaseModel


class LessonPlace(BaseModel):
    title = models.CharField(verbose_name='Lesson Place Title', max_length=32)
    link = models.CharField(verbose_name='Lesson Place Link', max_length=128, null=True, blank=True)


class Lesson(BaseModel):
    title = models.CharField(verbose_name='Lesson Title', max_length=64)
    type = models.CharField(verbose_name='Lesson Type', max_length=16)
    place = models.ForeignKey('schedule.LessonPlace', verbose_name='Lesson Place', on_delete=models.CASCADE)
    teachers = models.ManyToManyField('account.Teacher', related_name='lessons')


class ScheduledLesson(BaseModel):
    lesson = models.ForeignKey('schedule.Lesson', verbose_name='Lesson', on_delete=models.CASCADE)
    datetime = models.DateTimeField(verbose_name='Lesson DateTime')
