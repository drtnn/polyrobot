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

    # TODO: Временная реализация
    def get_first_or_create(self, delete_duplicates=False, *args, **kwargs):
        qs = self.filter(*args, **kwargs)
        if qs:
            obj = qs.first()

            if delete_duplicates:
                qs.exclude(id=obj.id).delete()
            return obj, False
        else:
            return self.create(*args, **kwargs), True


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = GetOrNoneManager()

    class Meta:
        abstract = True


class Timestampable(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
