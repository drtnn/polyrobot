# Generated by Django 4.0 on 2022-06-19 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0010_alter_lessonplace_title_alter_lessonroom_number_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scheduledlessonnotification',
            options={'verbose_name': 'Уведомление о начале занятия', 'verbose_name_plural': 'Уведомления о начале занятий'},
        ),
    ]