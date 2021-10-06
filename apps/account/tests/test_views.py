from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class RegistrationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.request_data = {
            'email': 'mobius@gmail.com',
            'password': 'mobius',
            'confirm_password': 'mobius'
        }
        self.response = self.client.post(
            reverse('registrations:register'),
            self.request_data,
            format="json")

    def test_registration_view_success(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_registration_view_fail(self):
        self.fail_request_data = {
            'email': 'mobius@gmail.com',
            'password': 'mobius'
        }

        self.response = self.client.post(
            reverse('registrations:register'),
            self.fail_request_data,
            format="json")

        self.assertEqual(self.response.status_code, 400)



