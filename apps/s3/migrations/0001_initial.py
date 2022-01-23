# Generated by Django 4.0 on 2022-01-23 07:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=64, verbose_name='File Title')),
                ('data', models.FileField(max_length=20971520, upload_to='', verbose_name='File Data')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
