from rest_framework import serializers
from apps.contact_book.models import *


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'surname', 'middle_name', 'nickname', 'name_pronunciation', 'pronouns', 'title',
                  'relation', 'company', 'job_title', 'side_notes', 'department', 'regularity_of_contact']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['email_address', 'label']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['state', 'country', 'postcode', 'address_line_one', 'address_line_two', 'suburb', 'city',
                  'start_of_habitation', 'end_of_habitation', 'is_current', 'is_hometown']


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['number', 'label']