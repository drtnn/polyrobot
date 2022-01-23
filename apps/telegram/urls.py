from rest_framework.routers import DefaultRouter

from .rest_api import TelegramUserViewSet

router = DefaultRouter()
router.register(r'telegram', TelegramUserViewSet, basename='telegram')
urlpatterns = router.urls
