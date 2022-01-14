from django.db import models
from django.utils.functional import cached_property

from apps.account.utils import MospolytechParser
from apps.core.models import BaseModel, Timestampable


# TODO: Шифровать поле password
class MospolytechUser(Timestampable):
    login = models.CharField(verbose_name='Mospolytech Login', max_length=32)
    password = models.CharField(verbose_name='Mospolytech Password', max_length=32)
    telegram_user = models.OneToOneField('telegram.TelegramUser', verbose_name='Telegram User',
                                         on_delete=models.CASCADE)
    cached_token = models.TextField(verbose_name='Cached Mospolytech Token')

    def token(self, cached=True) -> str:
        if not cached:
            self.cached_token = MospolytechParser.authenticate_mospolytech(self.login, self.password)
            self.save()
        return self.cached_token

    @cached_property
    def information(self) -> dict:
        return MospolytechParser.get_data_from_mospolytech(self, MospolytechParser.USER)

    @cached_property
    def schedule(self) -> dict:
        return MospolytechParser.get_data_from_mospolytech(self, MospolytechParser.SCHEDULE)

    @cached_property
    def payments(self) -> dict:
        return MospolytechParser.get_data_from_mospolytech(self, MospolytechParser.PAYMENTS)


class Group(BaseModel):
    number = models.CharField(verbose_name='Group Number', max_length=10)


class PersonalData(BaseModel):
    full_name = models.CharField(verbose_name='Full Name', max_length=64)


class Student(BaseModel):
    user = models.OneToOneField('account.MospolytechUser', verbose_name='User', on_delete=models.CASCADE)
    group = models.ForeignKey('account.Group', verbose_name='Group', on_delete=models.CASCADE)
    personal_data = models.ForeignKey('account.PersonalData', verbose_name='Personal Data', on_delete=models.CASCADE)


class Teacher(BaseModel):
    user = models.OneToOneField('account.MospolytechUser', verbose_name='User', on_delete=models.CASCADE)
    groups = models.ManyToManyField('account.Group', verbose_name='Groups')
    personal_data = models.ForeignKey('account.PersonalData', verbose_name='Personal Data', on_delete=models.CASCADE)
