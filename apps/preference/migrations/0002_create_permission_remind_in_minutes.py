# Generated by Django 4.0 on 2022-03-13 11:05

from django.db import migrations

from apps.preference.constants import REMIND_IN_MINUTES


def create_preference_remind_in_minutes(apps, schema_editor):
    Preference = apps.get_model('preference', 'Preference')

    Preference.objects.create(slug=REMIND_IN_MINUTES, default=15, max_value=90)


def create_user_preference_remind_in_minutes(apps, schema_editor):
    Preference = apps.get_model('preference', 'Preference')
    UserPreference = apps.get_model('preference', 'UserPreference')
    TelegramUser = apps.get_model('telegram', 'TelegramUser')

    preference = Preference.objects.get(slug=REMIND_IN_MINUTES)
    user_preferences = []
    for telegram_user in TelegramUser.objects.all():
        user_preferences.append(
            UserPreference(preference=preference, telegram_user=telegram_user, enabled=True, value=preference.default)
        )

    UserPreference.objects.bulk_create(user_preferences)


class Migration(migrations.Migration):
    dependencies = [
        ('preference', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(code=create_preference_remind_in_minutes),
        migrations.RunPython(code=create_user_preference_remind_in_minutes),
    ]
