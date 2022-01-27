from django.db import models

from apps.core.models import BaseModel


class LessonRoom(BaseModel):
    number = models.CharField(verbose_name='Lesson Room Number', max_length=16)


class LessonPlace(BaseModel):
    title = models.CharField(verbose_name='Lesson Place Title', max_length=32)
    rooms = models.ManyToManyField('schedule.LessonRoom', verbose_name='Lesson Rooms', related_name='lessons')
    link = models.CharField(verbose_name='Lesson Place Link', max_length=128, null=True, blank=True)


class LessonTeacher(BaseModel):
    full_name = models.CharField(verbose_name='Lesson Teacher', max_length=32)


class LessonType(BaseModel):
    title = models.CharField(verbose_name='Lesson Type', max_length=16)


class Lesson(BaseModel):
    title = models.CharField(verbose_name='Lesson Title', max_length=64)
    group = models.ForeignKey('mospolytech.Group', verbose_name='Group', on_delete=models.CASCADE)
    type = models.ForeignKey('schedule.LessonType', verbose_name='Lesson Type', on_delete=models.CASCADE)
    place = models.ForeignKey('schedule.LessonPlace', verbose_name='Lesson Place', on_delete=models.CASCADE)
    teachers = models.ManyToManyField('schedule.LessonTeacher', verbose_name='Lesson Teachers', related_name='lessons')


class ScheduledLesson(BaseModel):
    lesson = models.ForeignKey('schedule.Lesson', verbose_name='Lesson', on_delete=models.CASCADE)
    datetime = models.DateTimeField(verbose_name='Lesson DateTime')


class ScheduledLessonNote(BaseModel):
    scheduled_lesson = models.ForeignKey('schedule.ScheduledLesson', verbose_name='Scheduled Lesson',
                                         on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Scheduled Lesson Note Text', max_length=4096, blank=True, null=True)
    files = models.ManyToManyField('s3.File', verbose_name='Scheduled Lesson Note Files',
                                   related_name='scheduled_lesson_notes')
