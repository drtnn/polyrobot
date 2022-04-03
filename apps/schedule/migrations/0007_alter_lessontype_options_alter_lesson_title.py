# Generated by Django 4.0 on 2022-04-03 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_scheduledlessonnote_created_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lessontype',
            options={'verbose_name': 'Тип занятия', 'verbose_name_plural': 'Типы занятий'},
        ),
        migrations.AlterField(
            model_name='lesson',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Lesson Title'),
        ),
    ]
