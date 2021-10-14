from rest_framework import serializers
from apps.contact_book.models import *


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'surname', 'middle_name', 'nickname', 'name_pronunciation', 'pronouns', 'title',
                  'relation', 'company', 'job_title', 'side_notes', 'department', 'regularity_of_contact', 'last_time_contacted']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'email_address', 'label']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'state', 'country', 'postcode', 'address_line_one', 'address_line_two', 'suburb', 'city',
                  'start_of_habitation', 'end_of_habitation', 'is_current', 'is_hometown']


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['id', 'number', 'label']


class ImportantDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDate
        fields = ['date', 'get_alert', 'id', 'important_date_type']


class ImportantDateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDateType
        fields = ['label', 'icon']


class SocialMediaContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaContact
        fields = ['link', 'id', 'social_media_site']


class SocialMediaSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaSite
        fields = ['site', 'url_format', 'icon']