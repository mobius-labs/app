from django.urls import path

from apps.contact_book.api.views import (
    create_contact,
    get_contact_by_id
)

app_name = 'contact_book'

urlpatterns = [
    path('create_contact', create_contact, name="create_contact"),
    path('get_contact_by_id/<int:contact_id>', get_contact_by_id, name="create_contact")
]