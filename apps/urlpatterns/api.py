from django.urls import include, path

urlpatterns = [
    path('account/', include('apps.account.urls')),
    path('telegram/', include('apps.telegram.urls')),
]
