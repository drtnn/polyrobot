from django.urls import path, include
from rest_framework_nested import routers

from .rest_api import ScheduledLessonViewSet, ScheduledLessonNoteViewSet

scheduled_lesson = routers.SimpleRouter()
scheduled_lesson.register(r'scheduled-lesson', ScheduledLessonViewSet, basename='scheduled-lesson')

scheduled_lesson_note = routers.NestedSimpleRouter(scheduled_lesson, r'scheduled-lesson', lookup='scheduled_lesson')
scheduled_lesson_note.register(r'note', ScheduledLessonNoteViewSet, basename='note')

urlpatterns = [
    path(r'', include(scheduled_lesson.urls)),
    path(r'', include(scheduled_lesson_note.urls)),
]
