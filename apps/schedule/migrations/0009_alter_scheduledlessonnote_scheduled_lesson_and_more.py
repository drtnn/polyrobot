# Generated by Django 4.0 on 2022-04-08 05:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0004_alter_telegrammailing_keyboard'),
        ('schedule', '0008_alter_scheduledlessonnote_scheduled_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledlessonnote',
            name='scheduled_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to='schedule.scheduledlesson', verbose_name='Scheduled Lesson'),
        ),
        migrations.CreateModel(
            name='ScheduledLessonNotification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notify_at', models.DateTimeField(verbose_name='Lesson DateTime')),
                ('scheduled_lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications', to='schedule.scheduledlesson', verbose_name='Scheduled Lesson')),
                ('telegram_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_lesson_notifications', to='telegram.telegramuser', verbose_name='Telegram User')),
            ],
            options={
                'verbose_name': 'Уведомление о начале занятия',
                'verbose_name_plural': 'Уведомления о начале занятия',
            },
        ),
    ]