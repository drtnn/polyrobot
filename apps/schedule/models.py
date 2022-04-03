from datetime import timedelta

from django.db import models

from apps.core.models import BaseModel


class LessonRoom(BaseModel):
    number = models.CharField(verbose_name='Lesson Room Number', max_length=16)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'

    def __str__(self):
        return self.number


class LessonPlace(BaseModel):
    title = models.CharField(verbose_name='Lesson Place Title', max_length=64)
    rooms = models.ManyToManyField('schedule.LessonRoom', verbose_name='Lesson Rooms', related_name='lessons')
    link = models.CharField(verbose_name='Lesson Place Link', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'Место проведения'
        verbose_name_plural = 'Места проведения'

    def __str__(self):
        return self.title

    @property
    def rooms_str(self):
        return ', '.join([room.number for room in self.rooms.all()]) if self.rooms.all() else None


class LessonTeacher(BaseModel):
    full_name = models.CharField(verbose_name='Lesson Teacher', max_length=48)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return self.full_name


class LessonType(BaseModel):
    title = models.CharField(verbose_name='Lesson Type', max_length=16)

    class Meta:
        verbose_name = 'Тип занятия'
        verbose_name_plural = 'Типы занятий'

    def __str__(self):
        return self.title


class Lesson(BaseModel):
    title = models.CharField(verbose_name='Lesson Title', max_length=64)
    group = models.ForeignKey('mospolytech.Group', verbose_name='Group', on_delete=models.CASCADE)
    type = models.ForeignKey('schedule.LessonType', verbose_name='Lesson Type', on_delete=models.CASCADE)
    place = models.ForeignKey('schedule.LessonPlace', verbose_name='Lesson Place', on_delete=models.CASCADE)
    teachers = models.ManyToManyField('schedule.LessonTeacher', verbose_name='Lesson Teachers', related_name='lessons')

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return self.title

    @property
    def teachers_str(self):
        return ', '.join([teacher.full_name for teacher in self.teachers.all()]) if self.teachers.all() else None


class ScheduledLesson(BaseModel):
    lesson = models.ForeignKey('schedule.Lesson', verbose_name='Lesson', on_delete=models.CASCADE)
    datetime = models.DateTimeField(verbose_name='Lesson DateTime')

    class Meta:
        verbose_name = 'Запланированное занятие'
        verbose_name_plural = 'Запланированные занятия'

    def __str__(self):
        return str(self.lesson)

    @property
    def end_datetime(self):
        return self.datetime + timedelta(hours=1, minutes=30)


class ScheduledLessonNote(BaseModel):
    scheduled_lesson = models.ForeignKey('schedule.ScheduledLesson', verbose_name='Scheduled Lesson',
                                         on_delete=models.SET_NULL, null=True)
    text = models.TextField(verbose_name='Lesson Note Text', max_length=4096)
    files = models.ManyToManyField('s3.File', verbose_name='Lesson Note Files', related_name='scheduled_lesson_notes')
    created_by = models.ForeignKey('telegram.TelegramUser', verbose_name='Created by', on_delete=models.CASCADE,
                                   related_name='created_notes')

    class Meta:
        verbose_name = 'Заметка к запланированному занятию'
        verbose_name_plural = 'Заметки к запланированным занятиям'

    def __str__(self):
        return str(self.scheduled_lesson)

    @property
    def files_count(self):
        return str(self.files.all().count())
