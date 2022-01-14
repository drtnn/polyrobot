import uuid

from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class GetOrNoneManager(models.Manager):
        """Adds get_or_none method to objects
        """

        def get_or_none(self, **kwargs):
            try:
                return self.get(**kwargs)
            except self.model.DoesNotExist:
                return None

    class Meta:
        abstract = True


class Timestampable(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
