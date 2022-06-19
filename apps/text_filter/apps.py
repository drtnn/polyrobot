from django.apps import AppConfig


class TextFilterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.text_filter'
    verbose_name = 'Текстовые фильтры'

    def ready(self):
        import apps.text_filter.signals
