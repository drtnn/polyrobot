from django.urls import path

from apps.core import views

frontend_urlpatterns = [
    path('', views.index),
]
