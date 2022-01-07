from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MospolytechUser, Student, Group


@receiver([post_save], sender=MospolytechUser)
def save_mospolytech_user(sender, instance, **kwargs):
    if instance.information['user']['user_status'] == 'stud':
        group, _ = Group.objects.get_or_create(number=instance.information['user']['group'])
        Student.objects.update_or_create(user=instance, defaults={'group': group})
