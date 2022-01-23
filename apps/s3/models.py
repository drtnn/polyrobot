from django.db import models

from apps.core.storage_backends import PrivateMediaStorage
from apps.core.models import Timestampable


class File(Timestampable):
    data = models.FileField(verbose_name='File Data', storage=PrivateMediaStorage(), max_length=20_971_520)
