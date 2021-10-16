from django.test import TestCase
from apps.account.models import User
from apps.account.api.serializers import RegistrationSerializer
from rest_framework import serializers


class RegistrationSerializerTests(TestCase):
    def setUp(self):
        self.user_attributes = {
            'email': 'shiv@gmail.com',
            'password': 'shiv'
        }

        self.serializer_data = {
            'email': 'mobius@gmail.com',
            'password': 'mobius',
            'confirm_password': 'mobius'
        }

        self.user = User.objects.create(**self.user_attributes)
        self.serializer = RegistrationSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertCountEqual(data.keys(), ['email'])

    def test_email_field_content(self):
        data = self.serializer.data

        self.assertEqual(data['email'], self.user_attributes['email'])

    def test_valid(self):
        success_data = {
            'email': 'shiv@gmail.com',
            'password': 'shiv',
            'confirm_password': 'shiv'
        }
        fail_data = {
            'email': 'shiv@gmail.com',
            'password': 'shiv',
            'confirm_password': 'shivanah'
        }
        response = self.serializer.validate(success_data);
        self.assertEqual(response, success_data)

        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate(fail_data)

    def test_save(self):
        serializer = RegistrationSerializer(data=self.serializer_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            self.assertEqual(user.email, self.serializer_data['email'])
