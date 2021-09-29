from django.urls import path

from apps.contact_book.api.views import (
    create_contact_view
)

app_name = 'contact_book'

urlpatterns = [
    #path('get_contact', get_contact_view, name="get_contact"),
    path('create_contact', create_contact_view, name="create_contact")
]