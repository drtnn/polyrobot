from django.db import models

from apps.core.models import BaseModel


class Preference(BaseModel):
    slug = models.CharField(verbose_name='Preference Title', max_length=32, unique=True)
    default = models.SmallIntegerField(verbose_name='Preference Default Value', blank=True, null=True)
    max_value = models.SmallIntegerField(verbose_name='Preference Max Value', blank=True, null=True)

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return str(self.slug)


class UserPreference(BaseModel):
    preference = models.ForeignKey('Preference', verbose_name='Preference', related_name='user_preferences',
                                   on_delete=models.CASCADE)
    telegram_user = models.ForeignKey('telegram.TelegramUser', verbose_name='Telegram User', related_name='preferences',
                                      on_delete=models.CASCADE)
    enabled = models.BooleanField(verbose_name='Preference Enabled')
    value = models.PositiveSmallIntegerField(verbose_name='Preference Value', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользовательская настройка'
        verbose_name_plural = 'Пользовательские настройки'
        unique_together = ('preference', 'telegram_user',)

    def __str__(self):
        return str(self.preference)
