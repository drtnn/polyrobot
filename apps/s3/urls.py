from rest_framework.routers import DefaultRouter

from .rest_api import FileViewSet

app_name = 's3'
router = DefaultRouter()
router.register(r'file', FileViewSet, basename='file')
urlpatterns = router.urls
