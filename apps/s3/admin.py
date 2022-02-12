from django.contrib import admin

from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('data',)
    search_fields = ('data',)


admin.site.register(File, FileAdmin)
