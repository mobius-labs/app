from django.db import models

from apps.contact_book.models import Contact
# if importing doesn't work, just use 'Contact' not Contact in linked_to_contact_id line.


class User(models.Model):
    login_email = models.CharField(max_length=50, primary_key=True)
    date_created = models.DateTimeField()
    password = models.CharField(max_length=45)

    linked_to_contact_id = models.OneToOneField(Contact, on_delete=models.CASCADE)

