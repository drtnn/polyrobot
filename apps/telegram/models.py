from django.db import models

from apps.core.models import Timestampable


class TelegramUser(Timestampable):
    id = models.IntegerField(verbose_name='Telegram User ID', primary_key=True)
    username = models.CharField(verbose_name='Telegram Username', null=True, blank=True, max_length=32)
    full_name = models.CharField(verbose_name='Telegram Full Name', max_length=64)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.id)
