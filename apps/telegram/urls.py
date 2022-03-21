from django.urls import path, include
from rest_framework_nested import routers

from apps.schedule.rest_api import ScheduledLessonViewSet
from .rest_api import TelegramUserViewSet

telegram_router = routers.SimpleRouter()
telegram_router.register(r'telegram', TelegramUserViewSet, basename='telegram')

scheduled_lesson_router = routers.NestedSimpleRouter(telegram_router, r'telegram', lookup='telegram')
scheduled_lesson_router.register(r'scheduled-lesson', ScheduledLessonViewSet, basename='scheduled-lesson')

urlpatterns = [
    path(r'', include(telegram_router.urls)),
    path(r'', include(scheduled_lesson_router.urls)),
]
