from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MospolytechUser, Student, Group, PersonalData


@receiver([post_save], sender=MospolytechUser)
def save_mospolytech_user(sender, instance: MospolytechUser, **kwargs):
    user = instance.information()['user']
    if user['user_status'] == 'stud':
        group, _ = Group.objects.get_or_create(number=user['group'])

        if kwargs['created']:
            personal_data = PersonalData.objects.create(name=user['name'], surname=user['surname'],
                                                        patronymic=user['patronymic'])
        else:
            personal_data = instance.student.personal_data

        Student.objects.update_or_create(user=instance, personal_data=personal_data, defaults={'group': group})
