from django.urls import path

from apps.mospolytech import views as mospolytech_views

urlpatterns = [
    path('login-to-mospolytech/<int:telegram_id>/', mospolytech_views.login_to_mospolytech),
]
