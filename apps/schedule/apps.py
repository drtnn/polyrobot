from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.schedule'
    verbose_name = 'Расписание'

    def ready(self):
        import apps.schedule.signals
