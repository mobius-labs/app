from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from django.urls import reverse
from apps.contact_book.api.views import *
import datetime


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
        self.full_contact_serializer = FullContactSerializer(instance=self.contact)
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

        self.create_email_data = {
            'contact': self.contact,
            'email_address': 'moby123@gmail.com',
            'label': 'friend'
        }

        self.email = Email.objects.create(**self.create_email_data)
        self.email_serializer = EmailSerializer(instance=self.email)

        self.site_data = {
            'author_id': 'shiv@gmail.com',
            'site': 'Omegle'
        }
        self.new_site = SocialMediaSite.objects.create(**self.site_data)

        self.create_social_data = {
            'contact': self.contact,
            'social_media_site': self.new_site,
            'link': 'hello'
        }

        self.social = SocialMediaContact.objects.create(**self.create_social_data)
        self.social_serializer = SocialMediaContactSerializer(instance=self.social)

        self.datetype_data = {
            'label': 'anniversary',
            'icon': 'anniversary',
            'author_id': 'shiv@gmail.com'
        }

        self.datetype = ImportantDateType.objects.create(**self.datetype_data)
        self.datetype_serializer = ImportantDateTypeSerializer(instance=self.datetype)

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
        self.assertEqual(self.get_contact_response.data, self.full_contact_serializer.data)

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

    def test_get_emails(self):
        # create get request to get email
        self.get_email_request = self.request_factory.get(reverse('contacts:get_emails_by_cid',
                                                                  kwargs={'contact_id': self.contact_serializer.data[
                                                                      'id']}),
                                                          data={}, format='json')
        force_authenticate(self.get_email_request, user=self.user)

        self.get_email_response = get_emails_by_cid(self.get_email_request, self.contact_serializer.data['id'])
        self.assertEqual(self.get_email_response.status_code, status.HTTP_200_OK)

    def test_delete_email(self):
        self.new_email_data = {
            'email_address': 'shiv23@gmail.com',
            'label': 'business',
            'contact': self.contact
        }

        self.new_email = Email.objects.create(**self.new_email_data)
        self.new_email_serializer = EmailSerializer(instance=self.new_email)

        # create delete request to delete email
        self.delete_email_request = self.request_factory.delete(reverse('contacts:delete_email_by_eid',
                                                                        kwargs={'email_id':
                                                                                    self.new_email_serializer.data[
                                                                                        'id']}),
                                                                data={}, format='json')
        force_authenticate(self.delete_email_request, user=self.user)

        self.delete_email_response = delete_email_by_eid(self.delete_email_request,
                                                         self.new_email_serializer.data['id'])
        self.assertEqual(self.delete_email_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.delete_email_response.data, {'response': 'success'})

    def test_update_email(self):
        self.updated_email_data = {
            'email_address': 'moby321@gmail.com',
            'label': 'family'
        }

        # create update request to update email
        self.update_email_request = self.request_factory.put(reverse('contacts:update_email_by_eid',
                                                                     kwargs={
                                                                         'email_id': self.email_serializer.data[
                                                                             'id']}),
                                                             data=self.updated_email_data, format='json')
        force_authenticate(self.update_email_request, user=self.user)

        self.update_email_response = update_email_by_eid(self.update_email_request,
                                                         self.email_serializer.data['id'])
        self.assertEqual(self.update_email_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.update_email_response.data, {'response': 'success'})

    def test_create_site(self):
        self.new_site_data = {
            'author_id': 'shiv@gmail.com',
            'site': 'Reddit'
        }
        # create post request to create social media site
        self.create_site_request = self.request_factory.post(reverse('contacts:create_social_media_site'),
                                                             data=self.new_site_data, format='json')
        force_authenticate(self.create_site_request, user=self.user)

        self.create_site_response = create_social_media_site(self.create_site_request)
        self.assertEqual(self.create_site_response.status_code, status.HTTP_201_CREATED)

    def test_get_sites(self):
        # create get request to get sites
        self.get_site_request = self.request_factory.get(reverse('contacts:get_social_media_sites'),
                                                         data={}, format='json')
        force_authenticate(self.get_site_request, user=self.user)

        self.get_site_response = get_social_media_sites(self.get_site_request)
        self.assertEqual(self.get_site_response.status_code, status.HTTP_200_OK)

    def test_create_social(self):
        self.social_data = {
            'social_media_site': 'Facebook',
            'link': 'joerogan'
        }
        # create post request to create social media contact
        self.create_social_request = self.request_factory.post(reverse('contacts:create_social_media_contact',
                                                                       kwargs={
                                                                           'contact_id': self.contact_serializer.data[
                                                                               'id']}),
                                                               data=self.social_data, format='json')
        force_authenticate(self.create_social_request, user=self.user)

        self.create_social_response = create_social_media_contact(self.create_social_request,
                                                                  self.contact_serializer.data['id']
                                                                  )
        self.assertEqual(self.create_social_response.status_code, status.HTTP_201_CREATED)

    def test_get_social(self):
        # create get request to get social media contacts
        self.get_social_request = self.request_factory.get(reverse('contacts:get_socials_by_cid',
                                                                   kwargs={'contact_id': self.contact_serializer.data[
                                                                       'id']}),
                                                           data={}, format='json')
        force_authenticate(self.get_social_request, user=self.user)

        self.get_social_response = get_socials_by_cid(self.get_social_request, self.contact_serializer.data['id'])
        self.assertEqual(self.get_social_response.status_code, status.HTTP_200_OK)

    def test_delete_social(self):
        self.delete_site_data = {
            'author_id': 'shiv@gmail.com',
            'site': 'OnlyFans'
        }
        self.site_to_delete = SocialMediaSite.objects.create(**self.delete_site_data)

        self.new_social_data = {
            'link': 'troyesivan',
            'social_media_site': self.site_to_delete,
            'contact': self.contact
        }

        self.new_social = SocialMediaContact.objects.create(**self.new_social_data)
        self.new_social_serializer = SocialMediaContactSerializer(instance=self.new_social)

        # create delete request to delete social media contact
        self.delete_social_request = self.request_factory.delete(reverse('contacts:delete_social_by_sid',
                                                                         kwargs={'social_media_contact_id':
                                                                                     self.new_social_serializer.data[
                                                                                         'id']}),
                                                                 data={}, format='json')
        force_authenticate(self.delete_social_request, user=self.user)

        self.delete_social_response = delete_social_by_sid(self.delete_social_request,
                                                           self.new_social_serializer.data['id'])
        self.assertEqual(self.delete_social_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.delete_social_response.data, {'response': 'success'})

    def test_update_social(self):
        self.updated_social_data = {
            'social_media_site': 'Omegle',
            'link': 'hi'
        }

        # create update request to update social media contact
        self.update_social_request = self.request_factory.put(reverse('contacts:update_social_media_contact',
                                                                      kwargs={
                                                                          'social_media_contact_id':
                                                                              self.social_serializer.data[
                                                                                  'id']}),
                                                              data=self.updated_social_data, format='json')
        force_authenticate(self.update_social_request, user=self.user)

        self.update_social_response = update_social_media_contact(self.update_social_request,
                                                                  self.social_serializer.data['id'])
        self.assertEqual(self.update_social_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.update_social_response.data, {'response': 'success'})

    def test_create_datetype(self):
        self.new_datetype_data = {
            'label': 'festival',
            'icon': 'festival',
            'author_id': 'shiv@gmail.com'
        }
        # create post request to create datetype
        self.create_datetype_request = self.request_factory.post(reverse('contacts:create_important_date_type'),
                                                                 data=self.new_datetype_data, format='json')
        force_authenticate(self.create_datetype_request, user=self.user)

        self.create_datetype_response = create_important_date_type(self.create_datetype_request)
        self.assertEqual(self.create_datetype_response.status_code, status.HTTP_201_CREATED)

    def test_get_datetypes(self):
        # create get request to get datetypes
        self.get_datetype_request = self.request_factory.get(reverse('contacts:get_important_date_types'),
                                                           data={}, format='json')
        force_authenticate(self.get_datetype_request, user=self.user)

        self.get_datetype_response = get_important_date_types(self.get_datetype_request)
        self.assertEqual(self.get_datetype_response.status_code, status.HTTP_200_OK)

    def test_create_date(self):
        self.date_data = {
            'important_date_type': 'anniversary',
            'get_alert': True,
            'date': datetime.date(2021, 10, 19)
        }
        # create post request to create date
        self.create_date_request = self.request_factory.post(reverse('contacts:create_important_date',
                                                                    kwargs={'contact_id': self.contact_serializer.data[
                                                                       'id']}),
                                                                 data=self.date_data, format='json')
        force_authenticate(self.create_date_request, user=self.user)

        self.create_date_response = create_important_date(self.create_date_request, self.contact_serializer.data[
                                                                       'id'])
        self.assertEqual(self.create_date_response.status_code, status.HTTP_201_CREATED)


