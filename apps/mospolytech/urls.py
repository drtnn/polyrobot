from rest_framework.routers import DefaultRouter

from .rest_api import MospolytechUserViewSet

router = DefaultRouter()
router.register(r'mospolytech', MospolytechUserViewSet, basename='mospolytech')
urlpatterns = router.urls
