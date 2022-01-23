from django.urls import include, path

urlpatterns = [
    path('', include('apps.mospolytech.urls')),
    path('', include('apps.telegram.urls')),
    path('', include('apps.s3.urls')),
]
