# Generated by Django 4.0 on 2022-01-14 17:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='Lesson Title')),
                ('type', models.CharField(max_length=16, verbose_name='Lesson Type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LessonPlace',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='Lesson Place Title')),
                ('link', models.CharField(blank=True, max_length=128, null=True, verbose_name='Lesson Place Link')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScheduledLesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(verbose_name='Lesson DateTime')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.lesson', verbose_name='Lesson')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.lessonplace', verbose_name='Lesson Place'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='teachers',
            field=models.ManyToManyField(related_name='lessons', to='account.Teacher'),
        ),
    ]