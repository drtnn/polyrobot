from django.db import models
from django.utils.functional import cached_property

from apps.account.utils import authenticate_mospolytech, get_mospolytech_user, get_mospolytech_schedule, \
    get_mospolytech_payments
from apps.core.models import BaseModel, Timestampable


# TODO: Шифровать поле password
class MospolytechUser(Timestampable):
    login = models.CharField(verbose_name='Mospolytech Login', unique=True, max_length=100)
    password = models.TextField(verbose_name='Mospolytech Password', max_length=100)
    telegram_id = models.IntegerField(verbose_name='Telegram User ID', unique=True)

    @property
    def token(self):
        return authenticate_mospolytech(self.login, self.password)

    @cached_property
    def information(self):
        return get_mospolytech_user(self)

    @cached_property
    def schedule(self):
        return get_mospolytech_schedule(self)

    @cached_property
    def payments(self):
        return get_mospolytech_payments(self)


class Group(BaseModel):
    number = models.CharField(verbose_name='Group Number', max_length=10)


class Student(BaseModel):
    user = models.OneToOneField('MospolytechUser', verbose_name='User', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', verbose_name='Group', on_delete=models.CASCADE)


class Teacher(BaseModel):
    user = models.OneToOneField('MospolytechUser', verbose_name='User', on_delete=models.CASCADE)
    groups = models.ManyToManyField('Group', verbose_name='Groups')
