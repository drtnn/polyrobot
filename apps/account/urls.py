from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('login-to-mospolytech/', views.LoginToMospolytech.as_view(), name='login-to-mospolytech'),
]
