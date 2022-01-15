from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.mospolytech'

    def ready(self):
        import apps.mospolytech.signals
