from rest_framework import serializers
from apps.contact_book.models import *


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'surname', 'middle_name', 'nickname', 'name_pronunciation', 'pronouns', 'title',
                  'relation', 'company', 'job_title', 'side_notes', 'department', 'regularity_of_contact', 'last_time_contacted']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email_address', 'label']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['state', 'country', 'postcode', 'address_line_one', 'address_line_two', 'suburb', 'city',
                  'start_of_habitation', 'end_of_habitation', 'is_current', 'is_hometown']


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['number', 'label']


class ImportantDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDate
        fields = ['date', 'get_alert']


class ImportantDateOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDate
        fields = ['date', 'get_alert', 'contact', 'important_date_type']


class ImportantDateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDateType
        fields = ['label', 'icon', 'is_default']


class SocialMediaContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaContact
        fields = ['link']


class SocialMediaContactOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaContact
        fields = ['link', 'social_media_site']


class SocialMediaSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaSite
        fields = ['site', 'icon', 'is_default']