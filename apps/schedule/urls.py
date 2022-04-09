from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .rest_api import ScheduledLessonViewSet, ScheduledLessonNoteViewSet, ScheduledLessonNotificationViewSet

app_name = 'schedule'
router = DefaultRouter()
router.register(r'scheduled-lesson-note', ScheduledLessonNoteViewSet, basename='scheduled-lesson-note')
router.register(r'scheduled-lesson-notification', ScheduledLessonNotificationViewSet,
                basename='scheduled-lesson-notification')

scheduled_lesson = routers.SimpleRouter()
scheduled_lesson.register(r'scheduled-lesson', ScheduledLessonViewSet, basename='scheduled-lesson')

scheduled_lesson__note = routers.NestedSimpleRouter(scheduled_lesson, r'scheduled-lesson', lookup='scheduled_lesson')
scheduled_lesson__note.register(r'note', ScheduledLessonNoteViewSet, basename='note')

scheduled_lesson__notification = routers.NestedSimpleRouter(scheduled_lesson, r'scheduled-lesson',
                                                            lookup='scheduled_lesson')
scheduled_lesson__notification.register(r'notification', ScheduledLessonNotificationViewSet, basename='notification')

urlpatterns = router.urls + [
    path(r'', include(scheduled_lesson.urls)),
    path(r'', include(scheduled_lesson__note.urls)),
    path(r'', include(scheduled_lesson__notification.urls)),
]
