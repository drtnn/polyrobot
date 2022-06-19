from django.contrib import admin

from .models import BadWord


class BadWordAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)


admin.site.register(BadWord, BadWordAdmin)
