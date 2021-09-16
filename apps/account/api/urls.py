from django.urls import path
from apps.account.api.views import registration_view
# from .views import api views

app_name = "account"

urlpatterns = [
    path('register', registration_view, name="register")
]
