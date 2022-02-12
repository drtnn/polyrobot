from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import login_to_mospolytech
from .rest_api import MospolytechUserViewSet

router = DefaultRouter()
router.register(r'mospolytech', MospolytechUserViewSet, basename='mospolytech')
urlpatterns = router.urls

frontend_urlpatterns = [
    path('login-to-mospolytech/<int:telegram_id>/', login_to_mospolytech),
]
