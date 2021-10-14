from django.urls import path
from apps.account.api.views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = "account"

urlpatterns = [
    path('register', registration_view, name="register"),
    path('login', obtain_auth_token, name="login"),
    path('get_business_card_visibility', get_business_card_visibility, name="get_business_card_visibility"),
    path('update_business_card_visibility', update_business_card_visibility, name="update_business_card_visibility"),
    path('getinfo', get_info, name="getinfo")
]
