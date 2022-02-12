from django.urls import path, include

from apps.mospolytech.urls import frontend_urlpatterns as mospolytech_frontend_urlpatterns

urlpatterns = [
    path('', include(mospolytech_frontend_urlpatterns)),
]
