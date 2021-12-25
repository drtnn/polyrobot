import uuid

from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class Timestampable(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AuthUser(User, Timestampable):
    telegram_id = models.IntegerField(verbose_name='Telegram User ID', unique=True)


class Group(BaseModel):
    number = models.CharField(verbose_name='Second Group Number', max_length=10)


class Student(BaseModel):
    user = models.OneToOneField('AuthUser', verbose_name='User', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', verbose_name='Group', on_delete=models.CASCADE)


class Teacher(BaseModel):
    user = models.OneToOneField('AuthUser', verbose_name='User', on_delete=models.CASCADE)
    groups = models.ManyToManyField('Group', verbose_name='Groups')

