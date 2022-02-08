from rest_framework.routers import DefaultRouter

from .rest_api import MospolytechUserViewSet

router = DefaultRouter()
router.register(r'file', MospolytechUserViewSet, basename='file')
urlpatterns = router.urls
