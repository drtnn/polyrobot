from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MospolytechUser, Student, Group
from ..schedule.models import ScheduledLesson
from ..schedule.utils import save_schedule


@receiver([post_save], sender=MospolytechUser)
def save_mospolytech_user(sender, instance: MospolytechUser, **kwargs):
    user = instance.profile()['user']
    if user['user_status'] == 'stud':
        group, _ = Group.objects.get_or_create(number=user['group'])

        Student.objects.update_or_create(user=instance, defaults={'group': group})

        if not ScheduledLesson.objects.filter(lesson__group=group).exists():
            schedule = instance.schedule(is_session=False)
            session_schedule = instance.schedule(is_session=True)

            if isinstance(schedule, dict) and schedule.get('status') != 'error':
                save_schedule(group, schedule)
            if isinstance(session_schedule, dict) and session_schedule.get('status') != 'error':
                save_schedule(group, session_schedule)
