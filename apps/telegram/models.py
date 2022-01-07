from django.db import models

from apps.core.models import Timestampable


class GetOrNoneManager(models.Manager):
    """Adds get_or_none method to objects
    """

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class TelegramUser(Timestampable):
    telegram_id = models.IntegerField(verbose_name='Telegram User ID', unique=True)
    username = models.CharField(verbose_name='Telegram Username', null=True, blank=True, max_length=32)
    full_name = models.CharField(verbose_name='Telegram Full Name', max_length=64)

    objects = GetOrNoneManager()
