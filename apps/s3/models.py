from django.db import models

from apps.core.models import Timestampable
from apps.core.storage_backends import PrivateMediaStorage


class File(Timestampable):
    data = models.FileField(verbose_name='File Data', storage=PrivateMediaStorage())

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.data.name
