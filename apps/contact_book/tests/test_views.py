from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from django.urls import reverse
from rest_framework.test import APIClient
from apps.contact_book.api.views import *


class ContactViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='shiv@gmail.com', password='mobius')

        self.create_contact_request_data = {
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
            'regularity_of_contact': '2',
        }

        self.request_factory = APIRequestFactory()

        self.contact = Contact.objects.create(**self.create_contact_request_data)
        self.contact_serializer = ContactSerializer(instance=self.contact)

        self.create_phone_data = {
            'contact': self.contact,
            'number': '0487654321',
            'label': 'friend'
        }

        self.phone = Number.objects.create(**self.create_phone_data)
        self.phone_serializer = NumberSerializer(instance=self.phone)

        self.create_address_data = {
            'contact': self.contact,
            'address_line_one': '1 Elm Street',
            'suburb': 'Kruegertown'
        }

        self.address = Address.objects.create(**self.create_address_data)
        self.address_serializer = AddressSerializer(instance=self.address)

    def test_create_contact(self):
        # create post request to create contact
        self.create_contact_request = self.request_factory.post(reverse('contacts:create_contact'),
                                                                data=self.create_contact_request_data, format='json')
        force_authenticate(self.create_contact_request, user=self.user)

        self.create_contact_response = create_contact(self.create_contact_request)
        self.assertEqual(self.create_contact_response.status_code, status.HTTP_201_CREATED)

    def test_get_contact(self):
        # create get request to get contact
        self.get_contact_request = self.request_factory.get(reverse('contacts:get_contact_by_id',
                                                                    kwargs={'contact_id': self.contact_serializer.data[
                                                                        'id']}),
                                                            data={}, format='json')
        force_authenticate(self.get_contact_request, user=self.user)

        self.get_contact_response = get_contact_by_id(self.get_contact_request, self.contact_serializer.data['id'])
        self.assertEqual(self.get_contact_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.get_contact_response.data, self.contact_serializer.data)

    def test_delete_contact(self):
        self.new_contact_data = {
            'author_id': 'shiv@gmail.com',
            'first_name': 'mobius',
            'surname': 'labs',
            'middle_name': ' ',
            'nickname': 'moby',
            'name_pronunciation': 'moh-bee-us',
            'pronouns': 'they/them',
            'title': ' ',
            'relation': 'friend',
            'company': 'mobius labs',
            'job_title': 'boss',
            'side_notes': 'they\'re an up and coming CRM',
            'department': 'connection',
            'regularity_of_contact': '2',
        }

        self.new_contact = Contact.objects.create(**self.new_contact_data)
        self.new_contact_serializer = ContactSerializer(instance=self.new_contact)

        # create delete request to delete contact
        self.delete_contact_request = self.request_factory.delete(reverse('contacts:delete_contact_by_id',
                                                                          kwargs={'contact_id':
                                                                                      self.new_contact_serializer.data[
                                                                                          'id']}),
                                                                  data={}, format='json')
        force_authenticate(self.delete_contact_request, user=self.user)

        self.delete_contact_response = delete_contact_by_id(self.delete_contact_request,
                                                            self.new_contact_serializer.data['id'])
        self.assertEqual(self.delete_contact_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.delete_contact_response.data, {'response': 'success'})

    def test_update_contact(self):
        self.create_contact_request_data['first_name'] = 'shiv'

        # create update request to update contact details
        self.update_contact_request = self.request_factory.put(reverse('contacts:update_contact_by_id',
                                                                       kwargs={
                                                                           'contact_id': self.contact_serializer.data[
                                                                               'id']}),
                                                               data=self.create_contact_request_data, format='json')
        force_authenticate(self.update_contact_request, user=self.user)

        self.update_contact_response = update_contact_by_id(self.update_contact_request,
                                                            self.contact_serializer.data['id'])
        self.assertEqual(self.update_contact_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.update_contact_response.data, {'response': 'success'})

    def test_create_phone_no(self):
        self.phone_data = {
            'number': '0412345678',
            'label': 'business'
        }

        # create post request to create new phone number
        self.create_phone_no_request = self.request_factory.post(reverse('contacts:create_phone_no',
                                                                         kwargs={
                                                                             'contact_id': self.contact_serializer.data[
                                                                                 'id']}),
                                                                 data=self.phone_data, format='json')
        force_authenticate(self.create_phone_no_request, user=self.user)

        self.create_phone_no_response = create_phone_no(self.create_phone_no_request,
                                                        self.contact_serializer.data['id'])
        self.assertEqual(self.create_phone_no_response.status_code, status.HTTP_201_CREATED)

    def test_get_phone_no(self):
        # create get request to get phone number
        self.get_phone_no_request = self.request_factory.get(reverse('contacts:get_phones_no_by_cid',
                                                                     kwargs={'contact_id': self.contact_serializer.data[
                                                                         'id']}),
                                                             data={}, format='json')
        force_authenticate(self.get_phone_no_request, user=self.user)

        self.get_phone_response = get_phone_nos_by_cid(self.get_phone_no_request, self.contact_serializer.data['id'])
        self.assertEqual(self.get_phone_response.status_code, status.HTTP_200_OK)

    def test_delete_phone_no(self):
        self.new_phone_data = {
            'contact': self.contact,
            'number': '0423456789',
            'label': 'family'
        }

        self.new_phone = Number.objects.create(**self.new_phone_data)
        self.new_phone_serializer = NumberSerializer(instance=self.new_phone)

        # create delete request to delete phone number
        self.delete_phone_request = self.request_factory.delete(reverse('contacts:delete_phone_no_by_pid',
                                                                        kwargs={'number_id':
                                                                                    self.new_phone_serializer.data[
                                                                                        'id']}),
                                                                data={}, format='json')
        force_authenticate(self.delete_phone_request, user=self.user)

        self.delete_phone_response = delete_phone_no_by_pid(self.delete_phone_request,
                                                            self.new_phone_serializer.data['id'])
        self.assertEqual(self.delete_phone_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.delete_phone_response.data, {'response': 'success'})

    def test_update_phone_no(self):
        self.updated_phone_data = {
            'number': '0467892345',
            'label': 'friend'
        }

        # create update request to update phone number
        self.update_phone_request = self.request_factory.put(reverse('contacts:update_phone_no_by_pid',
                                                                     kwargs={
                                                                         'number_id': self.phone_serializer.data[
                                                                             'id']}),
                                                             data=self.updated_phone_data, format='json')
        force_authenticate(self.update_phone_request, user=self.user)

        self.update_phone_response = update_phone_no_by_pid(self.update_phone_request,
                                                            self.phone_serializer.data['id'])
        self.assertEqual(self.update_phone_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.update_phone_response.data, {'response': 'success'})

    def test_create_address(self):
        self.address_data = {
            'address_line_one': '1 Moby Lane',
            'suburb': 'Usville'
        }
        # create post request to create address
        self.create_address_request = self.request_factory.post(reverse('contacts:create_address',
                                                                        kwargs={
                                                                            'contact_id': self.contact_serializer.data[
                                                                                'id']}),
                                                                data=self.address_data, format='json')
        force_authenticate(self.create_address_request, user=self.user)

        self.create_address_response = create_address(self.create_address_request,
                                                      self.contact_serializer.data['id']
                                                      )
        self.assertEqual(self.create_address_response.status_code, status.HTTP_201_CREATED)

    def test_get_address(self):
        # create get request to get address
        self.get_address_request = self.request_factory.get(reverse('contacts:get_addresses_by_cid',
                                                                    kwargs={'contact_id': self.contact_serializer.data[
                                                                        'id']}),
                                                            data={}, format='json')
        force_authenticate(self.get_address_request, user=self.user)

        self.get_address_response = get_addresses_by_cid(self.get_address_request, self.contact_serializer.data['id'])
        self.assertEqual(self.get_address_response.status_code, status.HTTP_200_OK)

    def test_delete_address(self):
        self.new_address_data = {
            'contact': self.contact,
            'address_line_one': '1 Bar Street',
            'suburb': 'Foodale'
        }

        self.new_address = Address.objects.create(**self.new_address_data)
        self.new_address_serializer = AddressSerializer(instance=self.new_address)

        # create delete request to delete address
        self.delete_address_request = self.request_factory.delete(reverse('contacts:delete_address_by_aid',
                                                                          kwargs={'address_id':
                                                                                      self.new_address_serializer.data[
                                                                                          'id']}),
                                                                  data={}, format='json')
        force_authenticate(self.delete_address_request, user=self.user)

        self.delete_address_response = delete_address_by_aid(self.delete_address_request,
                                                             self.new_address_serializer.data['id'])
        self.assertEqual(self.delete_address_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.delete_address_response.data, {'response': 'success'})

    def test_update_address(self):
        self.updated_address_data = {
            'address_line_one': '1 Elm Street',
            'suburb': 'Freddy Falls'
        }

        # create update request to update address
        self.update_address_request = self.request_factory.put(reverse('contacts:update_address_by_aid',
                                                                       kwargs={
                                                                           'address_id': self.address_serializer.data[
                                                                               'id']}),
                                                               data=self.updated_address_data, format='json')
        force_authenticate(self.update_address_request, user=self.user)

        self.update_address_response = update_address_by_aid(self.update_address_request,
                                                             self.address_serializer.data['id'])
        self.assertEqual(self.update_address_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.update_address_response.data, {'response': 'success'})

    def test_create_email(self):
        self.email_data = {
            'email_address': 'moby@us.com',
            'label': 'business'
        }
        # create post request to create email
        self.create_email_request = self.request_factory.post(reverse('contacts:create_email',
                                                                      kwargs={
                                                                          'contact_id': self.contact_serializer.data[
                                                                              'id']}),
                                                              data=self.email_data, format='json')
        force_authenticate(self.create_email_request, user=self.user)

        self.create_email_response = create_email(self.create_email_request,
                                                  self.contact_serializer.data['id']
                                                      )
        self.assertEqual(self.create_email_response.status_code, status.HTTP_201_CREATED)

