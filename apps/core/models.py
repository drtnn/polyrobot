import uuid

from django.contrib.auth.models import User
from django.db import models


class GetOrNoneManager(models.Manager):
    """Adds get_or_none method to objects
    """

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = GetOrNoneManager()

    class Meta:
        abstract = True


class Timestampable(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
