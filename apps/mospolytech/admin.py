from django.contrib import admin

from apps.mospolytech.models import MospolytechUser, Group, PersonalData, Student, Teacher


class MospolytechUserAdmin(admin.ModelAdmin):
    list_display = ('login', 'telegram')
    search_fields = ('login', 'telegram')

    list_filter = ('student__group',)

    exclude = ('password', 'cached_token')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)


class PersonalDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'patronymic')
    search_fields = ('name', 'surname', 'patronymic')

    list_filter = ('name', 'surname', 'patronymic')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'personal_data')
    search_fields = ('user', 'group', 'personal_data')

    list_filter = ('group',)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'groups_str', 'personal_data')
    search_fields = ('user', 'groups', 'personal_data')

    list_filter = ('groups',)


admin.site.register(MospolytechUser, MospolytechUserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(PersonalData, PersonalDataAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
