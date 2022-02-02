from django.contrib import admin

from apps.telegram.models import TelegramUser


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'full_name')
    search_fields = ('id', 'username', 'full_name')

    list_filter = ('id', 'username', 'full_name')


admin.site.register(TelegramUser, TelegramUserAdmin)
