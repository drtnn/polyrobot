from django.db import models

from apps.core.models import BaseModel


class BadWord(BaseModel):
    text = models.CharField(verbose_name='Bad word text', max_length=32, unique=True)

    class Meta:
        verbose_name = 'Запрещенное сочетание букв'
        verbose_name_plural = 'Запрещенные сочетания букв'

    def __str__(self):
        return self.text
