from datetime import timedelta

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .constants import REMIND_IN_MINUTES
from .models import UserPreference, Preference
from ..schedule.models import ScheduledLesson, ScheduledLessonNotification
from ..telegram.models import TelegramUser


def create_scheduled_lesson_notifications(instance: UserPreference):
    telegram_user = instance.telegram_user
    ScheduledLessonNotification.objects.filter(telegram_user=telegram_user).delete()
    scheduled_lesson_notifications_to_create = []

    if not telegram_user.preferences.get(preference__slug=REMIND_IN_MINUTES).enabled:
        return

    remind_in_minutes = telegram_user.preferences.get(preference__slug=REMIND_IN_MINUTES).value
    for scheduled_lesson in ScheduledLesson.objects.filter(lesson__group=telegram_user.mospolytechuser.student.group):
        notify_at = scheduled_lesson.datetime - timedelta(minutes=remind_in_minutes)
        scheduled_lesson_notifications_to_create.append(
            ScheduledLessonNotification(
                scheduled_lesson=scheduled_lesson, telegram_user=telegram_user, notify_at=notify_at
            )
        )
    ScheduledLessonNotification.objects.bulk_create(scheduled_lesson_notifications_to_create)


def create_user_preferences(instance: Preference):
    user_preferences = []
    for telegram_user in TelegramUser.objects.all():
        user_preferences.append(
            UserPreference(preference=instance, telegram_user=telegram_user, enabled=True, value=instance.default)
        )
    UserPreference.objects.bulk_create(user_preferences)


@receiver([pre_save], sender=UserPreference)
def pre_save_user_preference(sender, instance: UserPreference, **kwargs):
    are_none = (instance.value is not None and instance.preference.max_value is not None)
    are_not_none = (instance.value is None and instance.preference.max_value is None)
    assert are_none or are_not_none, \
        f"UserPreference Value must {'not ' if instance.preference.max_value is not None else ''}be None"

    if instance.value and instance.preference.max_value:
        assert instance.value < instance.preference.max_value, "UserPreference Value is more than Preference"


@receiver([post_save], sender=UserPreference)
def post_save_user_preference(sender, instance: UserPreference, **kwargs):
    if instance.preference.slug == REMIND_IN_MINUTES:
        create_scheduled_lesson_notifications(instance=instance)


@receiver([post_save], sender=Preference)
def post_save_preference(sender, instance: Preference, **kwargs):
    create_user_preferences(instance=instance)
