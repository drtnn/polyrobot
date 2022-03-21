from rest_framework.routers import DefaultRouter

from .rest_api import FileViewSet

router = DefaultRouter()
router.register(r'file', FileViewSet, basename='file')
urlpatterns = router.urls
