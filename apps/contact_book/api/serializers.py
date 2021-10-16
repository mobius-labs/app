from rest_framework import serializers
from apps.contact_book.models import *


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'surname', 'middle_name', 'nickname', 'name_pronunciation', 'pronouns', 'title',
                  'relation', 'company', 'job_title', 'side_notes', 'department', 'regularity_of_contact',
                  'last_time_contacted', 'id']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email_address', 'label', 'id']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['state', 'country', 'postcode', 'address_line_one', 'address_line_two', 'suburb', 'city',
                  'start_of_habitation', 'end_of_habitation', 'is_current', 'is_hometown', 'id']


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['number', 'label', 'id']


class ImportantDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDate
        fields = ['date', 'get_alert', 'id']


class ImportantDateOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDate
        fields = ['date', 'get_alert', 'contact', 'important_date_type', 'id']


class ImportantDateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDateType
        fields = ['label', 'icon', 'is_default']


class SocialMediaContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaContact
        fields = ['link', 'id']


class SocialMediaContactOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaContact
        fields = ['link', 'social_media_site',]


class SocialMediaSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaSite
        fields = ['site', 'url_format', 'icon', 'id']


class FullContactSerializer(serializers.ModelSerializer):
    emails = EmailSerializer(many=True, source='email_set', read_only=True)
    addresses = AddressSerializer(many=True, source='address_set', read_only=True)
    phone_nos = NumberSerializer(many=True, source='number_set', read_only=True)
    important_dates = ImportantDateSerializer(many=True, source='importantdate_set', read_only=True)
    social_media = SocialMediaContactSerializer(many=True, source='socialmediacontact_set', read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'surname', 'middle_name', 'nickname', 'name_pronunciation', 'pronouns', 'title',
                  'relation', 'company', 'job_title', 'side_notes', 'department', 'regularity_of_contact',
                  'last_time_contacted', 'emails', 'addresses', 'phone_nos', 'important_dates', 'social_media')


