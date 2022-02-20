from django.contrib import admin

from apps.schedule.models import LessonRoom, LessonPlace, LessonTeacher, LessonType, Lesson, ScheduledLesson, \
    ScheduledLessonNote


class LessonRoomAdmin(admin.ModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)


class LessonPlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'rooms_str', 'link')
    search_fields = ('title', 'rooms__number', 'link')

    list_filter = ('title',)


class LessonTeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)


class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'type', 'place', 'teachers_str')
    search_fields = ('title', 'group__number', 'type__title', 'place__title', 'teachers__full_name')

    list_filter = ('title', 'group__number', 'type__title', 'place__title', 'teachers__full_name')


class ScheduledLessonAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'datetime')
    search_fields = ('lesson__title', 'datetime')

    list_filter = ('lesson__title', 'datetime')


class ScheduledLessonNoteAdmin(admin.ModelAdmin):
    list_display = ('scheduled_lesson', 'text', 'files_count')
    search_fields = ('scheduled_lesson__lesson__title', 'scheduled_lesson__datetime', 'text')

    list_filter = ('scheduled_lesson__lesson__title', 'scheduled_lesson__datetime')


admin.site.register(LessonRoom, LessonRoomAdmin)
admin.site.register(LessonPlace, LessonPlaceAdmin)
admin.site.register(LessonTeacher, LessonTeacherAdmin)
admin.site.register(LessonType, LessonTypeAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(ScheduledLesson, ScheduledLessonAdmin)
admin.site.register(ScheduledLessonNote, ScheduledLessonNoteAdmin)
