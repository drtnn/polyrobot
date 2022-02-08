from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import File


@receiver([post_delete], sender=File)
def save_mospolytech_user(sender, instance: File, **kwargs):
    instance.data.delete()
