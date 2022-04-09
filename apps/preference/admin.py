from django.contrib import admin

from apps.preference.models import Preference, UserPreference


class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('slug', 'default', 'max_value')
    search_fields = ('slug', 'default', 'max_value')

    list_filter = ('default', 'max_value')


class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('preference', 'telegram_user', 'enabled', 'value')
    search_fields = ('preference__slug', 'telegram_user__username', 'telegram_user__full_name', 'telegram_user__id',
                     'enabled', 'value')

    list_filter = ('preference', 'telegram_user', 'enabled', 'value')


admin.site.register(Preference, PreferenceAdmin)
admin.site.register(UserPreference, UserPreferenceAdmin)
