from rest_framework.routers import DefaultRouter

from .rest_api import TelegramUserViewSet

router = DefaultRouter()
router.register(r'user', TelegramUserViewSet, basename='user')
urlpatterns = router.urls
