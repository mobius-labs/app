from django.test import TestCase
from apps.contact_book.models import *
from apps.account.models import User
from apps.contact_book.api.serializers import *


class ContactBookSerializerTests(TestCase):
    def setUp(self):
        self.user_attributes = {
            'email': 'shiv@gmail.com',
            'password': 'shiv'
        }

        self.user = User.objects.create(**self.user_attributes)

        self.contact_attributes = {
            'author_id': 'shiv@gmail.com',
            'first_name': 'shivanah',
            'surname': 'shetty',
            'middle_name': ' ',
            'nickname': 'shiv',
            'name_pronunciation': 'shuh-vah-nah',
            'pronouns': 'she/her',
            'title': 'Miss',
            'relation': 'friend',
            'company': 'mobius labs',
            'job_title': 'developer',
            'side_notes': 'Shes pretty cool',
            'department': 'testing',
            'regularity_of_contact': '104',
        }

        self.contact_serializer_data = {
            'first_name': 'member',
            'surname': 'two',
            'middle_name': ' ',
            'nickname': 'mem',
            'name_pronunciation': 'mem-buh too',
            'pronouns': 'FEM',
            'title': 'Miss',
            'relation': 'associate',
            'company': 'google',
            'job_title': 'programmer',
            'side_notes': 'Shes ok',
            'department': 'robotics',
            'regularity_of_contact': 'WK1',
        }

        self.contact = Contact.objects.create(**self.contact_attributes)
        self.contact_serializer = ContactSerializer(instance=self.contact)

        self.email_attributes = {
            'email_address': 'shiv@gmail.com',
            'label': 'FRN',
            'id': '3',
            'contact': self.contact
        }

        self.email_serializer_data = {
            'email_address': 'mobius@gmail.com',
            'label': 'BUS',
        }

        self.email = Email.objects.create(**self.email_attributes)
        self.email_serializer = EmailSerializer(instance=self.email)

    def test_contact_serializer_contains_expected_fields(self):
        data = self.contact_serializer.data

        self.assertCountEqual(data.keys(), ['id', 'first_name', 'surname', 'middle_name', 'nickname', 'name_pronunciation',
                                            'pronouns', 'title', 'relation', 'company', 'job_title', 'side_notes',
                                            'department', 'regularity_of_contact', 'last_time_contacted'])

    def test_first_name_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['first_name'], self.contact_attributes['first_name'])

    def test_surname_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['surname'], self.contact_attributes['surname'])

    def test_middle_name_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['middle_name'], self.contact_attributes['middle_name'])

    def test_nickname_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['nickname'], self.contact_attributes['nickname'])

    def test_name_pronunciation_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['name_pronunciation'], self.contact_attributes['name_pronunciation'])

    def test_pronouns_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['pronouns'], self.contact_attributes['pronouns'])

    def test_title_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['title'], self.contact_attributes['title'])

    def test_relation_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['relation'], self.contact_attributes['relation'])

    def test_company_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['company'], self.contact_attributes['company'])

    def test_job_title_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['job_title'], self.contact_attributes['job_title'])

    def test_side_notes_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['side_notes'], self.contact_attributes['side_notes'])

    def test_department_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['department'], self.contact_attributes['department'])

    def test_regularity_of_contact_field_content(self):
        data = self.contact_serializer.data

        self.assertEqual(data['regularity_of_contact'], 104)

    def test_email_serializer_contains_expected_fields(self):
        data = self.email_serializer.data

        self.assertCountEqual(data.keys(), ['id', 'email_address', 'label'])

    def test_email_address_field_content(self):
        data = self.email_serializer.data

        self.assertEqual(data['email_address'], self.email_attributes['email_address'])

    def test_label_field_content(self):
        data = self.email_serializer.data

        self.assertEqual(data['label'], self.email_attributes['label'])

    def test_id_field_content(self):
        data = self.email_serializer.data

        self.assertEqual(data['id'], int(self.email_attributes['id']))
