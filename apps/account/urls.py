from rest_framework.routers import DefaultRouter

from .rest_api import MospolytechUserViewSet

router = DefaultRouter()
router.register(r'users', MospolytechUserViewSet, basename='user')
urlpatterns = router.urls
