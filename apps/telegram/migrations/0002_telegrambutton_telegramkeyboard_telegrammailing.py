# Generated by Django 4.0 on 2022-04-03 09:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramButton',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=128, verbose_name='Button Title')),
                ('link', models.TextField(verbose_name='Button Link')),
            ],
            options={
                'verbose_name': 'Кнопка',
                'verbose_name_plural': 'Кнопки',
            },
        ),
        migrations.CreateModel(
            name='TelegramKeyboard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='Keyboard Title')),
                ('row_width', models.SmallIntegerField(default=3, verbose_name='Telegram Keyboard Row Width')),
                ('buttons', models.ManyToManyField(related_name='keyboards', to='telegram.TelegramButton', verbose_name='Telegram Buttons')),
            ],
            options={
                'verbose_name': 'Клавиатура',
                'verbose_name_plural': 'Клавиатуры',
            },
        ),
        migrations.CreateModel(
            name='TelegramMailing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(verbose_name='Mailing Text')),
                ('keyboard', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mailings', to='telegram.telegramkeyboard', verbose_name='Mailing Keyboard')),
                ('telegram_users', models.ManyToManyField(related_name='mailings', to='telegram.TelegramUser', verbose_name='Mailing Users')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
    ]