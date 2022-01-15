from rest_framework.routers import DefaultRouter

from .rest_api import MospolytechUserViewSet

router = DefaultRouter()
router.register(r'user', MospolytechUserViewSet, basename='user')
urlpatterns = router.urls
