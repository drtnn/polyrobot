from django.apps import AppConfig


class PreferenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.preference'

    def ready(self):
        import apps.preference.signals
