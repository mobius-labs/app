from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.account.models import User


class RegistrationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.request_data = {
            'email': 'mobius@gmail.com',
            'password': 'mobius',
            'confirm_password': 'mobius'
        }
        self.register_response = self.client.post(
            reverse('registrations:register'),
            self.request_data,
            format="json")

        self.user = User.objects.get(email=self.register_response.data['email'])
        self.client.force_authenticate(user=self.user)

        self.get_info_response = self.client.get(
            reverse('registrations:getinfo'),
            format="json"
        )

        self.update_data = {
            'email': 'moby@gmail.com',
            'business_card': True,
            'business_card_theme': 'granite night'
        }

        self.update_bc_response = self.client.put(
            reverse('registrations:update_business_card_visibility'),
            self.update_data,
            format="json"
        )

        self.get_bc_response = self.client.get(
            reverse('registrations:get_business_card_visibility'),
            format="json"
        )

    def test_registration_view_success(self):
        self.assertEqual(self.register_response.status_code, status.HTTP_200_OK)

    def test_registration_view_fail(self):
        self.fail_request_data = {
            'email': 'mobius@gmail.com',
            'password': 'mobius'
        }

        self.failed_response = self.client.post(
            reverse('registrations:register'),
            self.fail_request_data,
            format="json")

        self.assertEqual(self.failed_response.status_code, 400)

    def test_get_info(self):
        self.assertEqual(self.get_info_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.get_info_response.data['email'], self.request_data['email'])

    def test_update_bc(self):
        self.assertEqual(self.update_bc_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.update_bc_response.data['response'], 'success')

    def test_get_bc(self):
        self.assertEqual(self.get_bc_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.get_bc_response.data['email'], self.request_data['email'])




