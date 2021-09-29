from rest_framework import serializers
from apps.contact_book.models import *


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact

        # From Django doc:
        # "By default, all the model fields on the class will be mapped to a corresponding serializer fields."
        # fields = ['id', 'account_name', 'users', 'created']



