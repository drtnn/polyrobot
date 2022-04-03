import logging

from django.contrib import admin
from django.shortcuts import redirect

from apps.telegram.bot import notify_admins, mailing_users
from apps.telegram.models import TelegramUser, TelegramMailing, TelegramButton, TelegramKeyboard

logger = logging.getLogger(__name__)


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'full_name')
    search_fields = ('id', 'username', 'full_name')

    list_filter = ('id', 'username', 'full_name')

    actions = ('mailing',)

    @admin.action(description='Создать рассылку')
    def mailing(self, request, queryset):
        mailing = TelegramMailing.objects.create(text='')
        mailing.telegram_users.add(*[telegram_user for telegram_user in queryset])
        mailing.save()
        return redirect("admin:telegram_telegrammailing_change", mailing.id)


class TelegramMailingAdmin(admin.ModelAdmin):
    list_display = ('text', 'telegram_users_str')
    search_fields = ('text',)

    list_filter = ('text', 'telegram_users')

    actions = ('activate',)

    @admin.action(description='Отправить')
    def activate(self, request, queryset):
        for mailing in queryset:
            if mailing.text.strip():
                count_of_successes, count_of_errors = mailing_users(telegram_user_queryset=mailing.telegram_users.all(),
                                                                    text=mailing.text, keyboard_object=mailing.keyboard)
                notify_admins(
                    text=f'{mailing.text}\n\nДоставлено: {count_of_successes}\nНе доставлено: {count_of_errors}')


class TelegramKeyboardAdmin(admin.ModelAdmin):
    list_display = ('title', 'row_width', 'buttons_str')
    search_fields = ('title',)

    list_filter = ('title', 'buttons')


class TelegramButtonAdmin(admin.ModelAdmin):
    list_display = ('text', 'link')
    search_fields = ('text', 'link')

    list_filter = ('text', 'link')


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramMailing, TelegramMailingAdmin)
admin.site.register(TelegramKeyboard, TelegramKeyboardAdmin)
admin.site.register(TelegramButton, TelegramButtonAdmin)
