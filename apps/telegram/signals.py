from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.preference.models import Preference, UserPreference
from apps.telegram.models import TelegramUser


def create_preferences(instance: TelegramUser):
    user_preferences_to_create = []
    for preference in Preference.objects.all():
        user_preferences_to_create.append(
            UserPreference(preference=preference, telegram_user=instance, enabled=True, value=preference.default)
        )
    UserPreference.objects.bulk_create(user_preferences_to_create)


@receiver([post_save], sender=TelegramUser)
def post_save_telegram_user(sender, instance: TelegramUser, **kwargs):
    if kwargs['created']:
        create_preferences(instance=instance)
