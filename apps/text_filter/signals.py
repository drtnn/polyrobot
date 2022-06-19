from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import BadWord


@receiver([pre_save], sender=BadWord)
def pre_save_scheduled_lesson(sender, instance: BadWord, **kwargs):
    instance.text = instance.text.lower()
