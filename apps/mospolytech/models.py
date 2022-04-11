from django.db import models
from encrypted_model_fields.fields import EncryptedCharField

from apps.core.models import BaseModel, Timestampable
from apps.mospolytech.utils import MospolytechParser
from apps.schedule.models import ScheduledLesson


class MospolytechUser(Timestampable):
    name = models.CharField(verbose_name='Name', max_length=32)
    surname = models.CharField(verbose_name='Surname', max_length=32)
    patronymic = models.CharField(verbose_name='Patronymic', max_length=32, null=True, blank=True)

    login = models.CharField(verbose_name='Mospolytech Login', max_length=64)
    password = EncryptedCharField(verbose_name='Mospolytech Password', max_length=256)
    cached_token = EncryptedCharField(verbose_name='Cached Mospolytech Token', max_length=256)

    telegram = models.OneToOneField('telegram.TelegramUser', verbose_name='Telegram User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.surname} {self.name}' + (f' {self.patronymic}' if self.patronymic else '')

    def token(self, cached=True) -> str:
        if not cached:
            self.cached_token = MospolytechParser.authenticate_mospolytech(self.login, self.password)
            self.save()
        return self.cached_token

    def profile(self) -> dict:
        return MospolytechParser.get_data_from_mospolytech(self, MospolytechParser.USER)

    def schedule(self, is_session: bool = False) -> dict:
        return MospolytechParser.get_data_from_mospolytech(self, MospolytechParser.SCHEDULE, session=int(is_session))

    def payments(self) -> dict:
        return MospolytechParser.get_data_from_mospolytech(self, MospolytechParser.PAYMENTS)

    def academic_performance(self, semester_number: int = None) -> dict:
        kwargs = {'semestr': semester_number} if semester_number else {}
        return MospolytechParser.get_data_from_mospolytech(self, MospolytechParser.ACADEMIC_PERFORMANCE, **kwargs)


class Group(BaseModel):
    number = models.CharField(verbose_name='Group Number', max_length=10)

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'

    def __str__(self):
        return self.number


class Student(BaseModel):
    user = models.OneToOneField('mospolytech.MospolytechUser', verbose_name='User', on_delete=models.CASCADE)
    group = models.ForeignKey('mospolytech.Group', verbose_name='Group', related_name='students',
                              on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return str(self.user)


class Teacher(BaseModel):
    user = models.OneToOneField('mospolytech.MospolytechUser', verbose_name='User', on_delete=models.CASCADE)
    groups = models.ManyToManyField('mospolytech.Group', related_name='teachers', verbose_name='Groups')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    @property
    def groups_str(self):
        return ', '.join([group.number for group in self.groups.all()]) if self.groups.all() else None

    def __str__(self):
        return str(self.user)
