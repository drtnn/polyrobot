from django.contrib import admin
from django.shortcuts import redirect

from apps.mospolytech.models import MospolytechUser, Group, Student, Teacher
from apps.telegram.models import TelegramMailing


class MospolytechUserAdmin(admin.ModelAdmin):
    list_display = ('login', 'telegram', 'name', 'surname', 'patronymic')
    search_fields = (
        'login', 'telegram__id', 'telegram__username', 'telegram__full_name', 'name', 'surname', 'patronymic'
    )

    list_filter = ('student__group',)

    exclude = ('password', 'cached_token')

    actions = ('mailing',)

    @admin.action(description='Создать рассылку')
    def mailing(self, request, queryset):
        mailing = TelegramMailing.objects.create(text='')
        mailing.telegram_users.add(*[user.telegram for user in queryset])
        mailing.save()
        return redirect("admin:telegram_telegrammailing_change", mailing.id)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)

    actions = ('mailing',)

    @admin.action(description='Создать рассылку для студентов')
    def mailing(self, request, queryset):
        mailing = TelegramMailing.objects.create(text='')
        for group in queryset:
            mailing.telegram_users.add(*[student.user.telegram for student in group.students.all()])
        mailing.save()
        return redirect("admin:telegram_telegrammailing_change", mailing.id)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    search_fields = ('user__login', 'group__number', 'user__name', 'user__surname', 'user__patronymic')
    list_filter = ('group',)

    actions = ('mailing',)

    @admin.action(description='Создать рассылку')
    def mailing(self, request, queryset):
        mailing = TelegramMailing.objects.create(text='')
        mailing.telegram_users.add(*[student.user.telegram for student in queryset])
        mailing.save()
        return redirect("admin:telegram_telegrammailing_change", mailing.id)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'groups_str')
    search_fields = ('user__login', 'groups__number', 'user__name', 'user__surname', 'user__patronymic')

    list_filter = ('groups',)

    actions = ('mailing',)

    @admin.action(description='Создать рассылку')
    def mailing(self, request, queryset):
        mailing = TelegramMailing.objects.create(text='')
        mailing.telegram_users.add(*[teacher.user.telegram for teacher in queryset])
        mailing.save()
        return redirect("admin:telegram_telegrammailing_change", mailing.id)


admin.site.register(MospolytechUser, MospolytechUserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
