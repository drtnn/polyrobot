from django.contrib import admin

from apps.mospolytech.models import MospolytechUser, Group, Student, Teacher


class MospolytechUserAdmin(admin.ModelAdmin):
    list_display = ('login', 'telegram')
    search_fields = (
        'login', 'telegram__id', 'telegram__username', 'telegram__full_name', 'name', 'surname', 'patronymic'
    )

    list_filter = ('student__group',)

    exclude = ('password', 'cached_token')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)


class StudentAdmin(admin.ModelAdmin):
    # list_display = ('user', 'group', 'user__full_name')
    search_fields = (
        'user__login', 'group__number', 'user__name', 'user__surname', 'user__patronymic'
    )
    list_filter = ('group',)


class TeacherAdmin(admin.ModelAdmin):
    # list_display = ('user', 'groups_str', 'user__full_name')
    search_fields = (
        'user__login', 'groups__number', 'user__name', 'user__surname', 'user__patronymic'
    )

    list_filter = ('groups',)


admin.site.register(MospolytechUser, MospolytechUserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
