from django.urls import include, path

urlpatterns = [
    path('mospolytech/', include('apps.mospolytech.urls')),
    path('telegram/', include('apps.telegram.urls')),
]
