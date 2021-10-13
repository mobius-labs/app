from django.urls import path
from apps.account.api.views import (
    registration_view, get_info
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = "account"

urlpatterns = [
    path('register', registration_view, name="register"),
    path('login', obtain_auth_token, name="login"),
    path('getinfo', get_info, name="getinfo")
]