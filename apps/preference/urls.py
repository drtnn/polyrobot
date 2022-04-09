from rest_framework.routers import DefaultRouter

from .rest_api import UserPreferenceViewSet

app_name = 'preference'
router = DefaultRouter()
router.register(r'user-preference', UserPreferenceViewSet, basename='user-preference')
urlpatterns = router.urls
