from datetime import timedelta, datetime

import pytz
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.preference.constants import REMIND_IN_MINUTES
from apps.telegram.models import TelegramUser
from .models import ScheduledLesson, ScheduledLessonNotification


def create_scheduled_lesson_notifications(instance: ScheduledLesson):
    scheduled_lesson_notifications_to_create = []
    for telegram_user in TelegramUser.objects.filter(mospolytechuser__student__group=instance.lesson.group):
        notify_at = instance.datetime - timedelta(
            minutes=telegram_user.preferences.get(preference__slug=REMIND_IN_MINUTES).value
        )
        scheduled_lesson_notifications_to_create.append(
            ScheduledLessonNotification(scheduled_lesson=instance, telegram_user=telegram_user, notify_at=notify_at)
        )
    ScheduledLessonNotification.objects.bulk_create(scheduled_lesson_notifications_to_create)


@receiver([post_save], sender=ScheduledLesson)
def post_save_scheduled_lesson(sender, instance: ScheduledLesson, **kwargs):
    instance.user_notifications.all().delete()
    tz = instance.datetime.tzinfo
    if instance.datetime > datetime.now(tz=tz):
        create_scheduled_lesson_notifications(instance=instance)
