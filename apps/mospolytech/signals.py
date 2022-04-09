from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.schedule.models import ScheduledLesson, ScheduledLessonNotification
from apps.schedule.utils import save_schedule
from .models import MospolytechUser, Student, Group
from ..preference.constants import REMIND_IN_MINUTES


def create_mospolytech_user_related_objects(instance: MospolytechUser):
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


def create_scheduled_lesson_notifications(instance: MospolytechUser):
    scheduled_lesson_notifications_to_create = []
    remind_in_minutes = instance.telegram.preferences.get(preference__slug=REMIND_IN_MINUTES).value
    for scheduled_lesson in ScheduledLesson.objects.filter(lesson__group=instance.student.group):
        notify_at = scheduled_lesson.datetime - timedelta(minutes=remind_in_minutes)
        scheduled_lesson_notifications_to_create.append(
            ScheduledLessonNotification(
                scheduled_lesson=scheduled_lesson, telegram_user=instance.telegram, notify_at=notify_at
            )
        )
    ScheduledLessonNotification.objects.bulk_create(scheduled_lesson_notifications_to_create)


@receiver([post_save], sender=MospolytechUser)
def post_save_mospolytech_user(sender, instance: MospolytechUser, **kwargs):
    create_mospolytech_user_related_objects(instance=instance)
    if kwargs['created']:
        create_scheduled_lesson_notifications(instance=instance)
