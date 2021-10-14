from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from django.urls import reverse
from rest_framework.test import APIClient
from apps.contact_book.api.views import *


class ContactViewTests(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(email='shiv@gmail.com', password='mobius')

        # self.client = APIClient()
        # self.client.login(email='shiv@gmail.com', password='mobius')
        # self.client.force_authenticate(user=self.user)
        self.request_data = {
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
            'regularity_of_contact': '2',
        }

        request_factory = APIRequestFactory()
        self.request = request_factory.post(reverse('contacts:create_contact'), data=self.request_data, format='json')
        force_authenticate(self.request, user=self.user)


        # self.response = self.client.post(
        #     reverse('contacts:create_contact'),
        #     self.request_data,
        #     format="json",
        # )

    def test_create_contact(self):

        # self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        # self.client.logout()
        self.response = create_contact(self.request)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


