from django.contrib import admin

from apps.schedule.models import LessonRoom, LessonPlace, LessonTeacher, LessonType, Lesson, ScheduledLesson, \
    ScheduledLessonNote


class LessonRoomAdmin(admin.ModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)


class LessonPlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'rooms_str', 'link')
    search_fields = ('title', 'rooms', 'link')

    list_filter = ('title',)


class LessonTeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)


class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'type', 'place', 'teachers_str')
    search_fields = ('title', 'group', 'type', 'place', 'teachers')

    list_filter = ('title', 'group', 'type', 'place', 'teachers')


class ScheduledLessonAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'datetime')
    search_fields = ('lesson', 'datetime')

    list_filter = ('lesson', 'datetime')


class ScheduledLessonNoteAdmin(admin.ModelAdmin):
    list_display = ('scheduled_lesson', 'text', 'files_count')
    search_fields = ('scheduled_lesson', 'text', 'files_count')

    list_filter = ('scheduled_lesson__lesson',)


admin.site.register(LessonRoom, LessonRoomAdmin)
admin.site.register(LessonPlace, LessonPlaceAdmin)
admin.site.register(LessonTeacher, LessonTeacherAdmin)
admin.site.register(LessonType, LessonTypeAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(ScheduledLesson, ScheduledLessonAdmin)
admin.site.register(ScheduledLessonNote, ScheduledLessonNoteAdmin)
