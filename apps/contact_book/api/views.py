import datetime

from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from apps.account.models import User
from apps.contact_book.api.serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.contact_book.models import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from datetime import date, timedelta

from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import date


NOT_PERMITTED_RESPONSE = {'has_permissions': False}
ALREADY_ADDED_RESPONSE = {'non_field_errors': ['This item already exists']}

# ---------------------------------------- CONTACTS ----------------------------------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_contact(request):
    user = request.user
    contact = Contact(author=user)

    serializer = ContactSerializer(contact, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_contact(request):
    user = request.user

    if user.connected_contact is not None:
        return Response(ALREADY_ADDED_RESPONSE, status=400)

    contact = Contact(author=user)

    serializer = ContactSerializer(contact, data=request.data)
    if serializer.is_valid():
        serializer.save()
        user.connected_contact = contact
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_contact_by_id(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    serializer = FullContactSerializer(contact)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_contacts(request):
    user = request.user
    contact = user.connected_contact
    if contact is None:
        return HttpResponse(status=404)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    serializer = FullContactSerializer(contact)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def get_business_cards(request, email):
    user = get_object_or_404(User, email=email)
    contact = user.connected_contact

    if user.business_card:
        serializer = FullContactSerializer(contact)
        data = serializer.data
        data['business_card_theme'] = user.business_card_theme
        return Response(data)
    else:
        return Response({"user's business card is not shareable"}, status=404)


class ApiContactList(ListAPIView):

    def get_queryset(self):
        user = self.request.user
        for_user = Contact.objects.filter(author=user.email)

        # exclude the user's own contact from this queryset
        if user.connected_contact is not None:
            for_user = for_user.exclude(pk=user.connected_contact.pk)
        return for_user

    queryset = Contact.objects.all()
    serializer_class = FullContactSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('first_name', 'surname', 'nickname')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_contact_by_id(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    operation = contact.delete()
    if operation:
        return Response({'response': 'success'})
    return Response({'response': 'unsuccessful'}, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_contact_by_id(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    serializer = ContactSerializer(contact, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'response': 'success'})
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


def calc_days_until_catchup(contact):
    # check to see if contact is overdue to be contacted
    if isinstance(contact.last_time_contacted, type(None)) or isinstance(contact.regularity_of_contact, type(None)):
        return False

    today = date.today()

    # decide whether contact should be shown for this window, find days until
    delta = contact.last_time_contacted - today + timedelta(days=365/contact.regularity_of_contact)
    return delta.days


class ApiCatchupCountdown(ListAPIView):

    def get_queryset(self):
        user = self.request.user
        days_window = self.kwargs['days_window']
        within_window = []

        # goes through all contacts and checks if they are overdue
        for contact in Contact.objects.all():
            days_until_catchup = calc_days_until_catchup(contact)
            if str(contact.author) == str(user.email) and days_until_catchup < days_window:
                within_window.append(contact)
        return within_window

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (OrderingFilter, )


# ---------------------------------------- PHONE NUMBERS ----------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_phone_no(request, contact_id):
    user = request.user

    # firstly check if the contact exists, and the contact was created by the author
    contact = get_object_or_404(Contact, id=contact_id)
    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    # then created the phone number
    phone_no = Number(contact=contact)
    serializer = NumberSerializer(phone_no, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(ALREADY_ADDED_RESPONSE, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phone_nos_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    numbers = list(Number.objects.all().filter(contact_id=contact))
    serializer = NumberSerializer(numbers, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_phone_no_by_pid(request, number_id):
    user = request.user
    number = get_object_or_404(Number, id=number_id)

    if str(number.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    operation = number.delete()
    if operation:
        return Response({'response': 'success'})
    return Response({'response': 'unsuccessful'}, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_phone_no_by_pid(request, number_id):
    user = request.user
    number = get_object_or_404(Number, id=number_id)

    if str(number.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    serializer = NumberSerializer(number, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'response': 'success'})
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


# ----------------------------------------- ADDRESSES -----------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_address(request, contact_id):
    user = request.user

    contact = get_object_or_404(Contact, id=contact_id)
    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    address = Address(contact=contact)
    serializer = AddressSerializer(address, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(ALREADY_ADDED_RESPONSE, status=400)
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_addresses_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    addresses = list(Address.objects.all().filter(contact_id=contact))
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_address_by_aid(request, address_id):
    user = request.user
    address = get_object_or_404(Address, id=address_id)

    if str(address.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    operation = address.delete()
    if operation:
        return Response({'response': 'success'})
    return Response({'response': 'unsuccessful'}, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_address_by_aid(request, address_id):
    user = request.user
    address = get_object_or_404(Address, id=address_id)

    if str(address.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    serializer = AddressSerializer(address, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'response': 'success'})
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


# ----------------------------------------- EMAILS -----------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_email(request, contact_id):
    user = request.user

    contact = get_object_or_404(Contact, id=contact_id)
    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    email = Email(contact=contact)
    serializer = EmailSerializer(email, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(ALREADY_ADDED_RESPONSE, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_emails_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    emails = list(Email.objects.all().filter(contact_id=contact))
    serializer = EmailSerializer(emails, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_email_by_eid(request, email_id):
    user = request.user
    email = get_object_or_404(Email, id=email_id)

    if str(email.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    operation = email.delete()
    if operation:
        return Response({'response': 'success'})
    return Response({'response': 'unsuccessful'}, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_email_by_eid(request, email_id):
    user = request.user
    email = get_object_or_404(Email, id=email_id)

    if str(email.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    serializer = EmailSerializer(email, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'response': 'success'})
        except IntegrityError:
            return Response(ALREADY_ADDED_RESPONSE, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


# ----------------------------------------- SOCIAL MEDIA SITE -----------------------------------------


@api_view(['POST'])
def create_social_media_site(request):
    social_media_site = SocialMediaSite()
    social_media_site.author = request.user
    serializer = SocialMediaSiteSerializer(social_media_site, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(ALREADY_ADDED_RESPONSE, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([])
def get_social_media_sites(request):
    sites = SocialMediaSite.objects.all().filter(author__isnull=True)
    if request.user is not None:
        sites = sites.union(SocialMediaSite.objects.all().filter(author=request.user))

    serializer = SocialMediaSiteSerializer(sites, many=True)
    return Response(serializer.data)


# ----------------------------------------- SOCIAL MEDIA -----------------------------------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_social_media_contact(request, contact_id):
    user = request.user

    contact = get_object_or_404(Contact, id=contact_id)
    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    # try to link social media link to relevant site
    if 'social_media_site' not in request.data:
        return Response({'errors': {'social_media_site': ['Social media site is required.']}}, status=400)
    social_media_site = SocialMediaSite.objects.get(site=request.data['social_media_site'])

    social_media_contact = SocialMediaContact(contact=contact, social_media_site=social_media_site)
    serializer = SocialMediaContactSerializer(social_media_contact, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(ALREADY_ADDED_RESPONSE, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_socials_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    socials = list(SocialMediaContact.objects.all().filter(contact_id=contact))
    serializer = SocialMediaContactSerializer(socials, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_social_by_sid(request, social_media_contact_id):
    user = request.user
    social_media_contact = get_object_or_404(SocialMediaContact, id=social_media_contact_id)

    if str(social_media_contact.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    operation = social_media_contact.delete()
    if operation:
        return Response({'response': 'success'})
    return Response({'response': 'unsuccessful'}, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_social_media_contact(request, social_media_contact_id):
    user = request.user
    social_media_contact = get_object_or_404(SocialMediaContact, id=social_media_contact_id)

    if str(social_media_contact.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    serializer = SocialMediaContactSerializer(social_media_contact, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'response': 'success'})
        except IntegrityError:
            return Response(ALREADY_ADDED_RESPONSE, status=400)
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


# ----------------------------------------- IMPORTANT DATE TYPE -----------------------------------------


@api_view(['POST'])
def create_important_date_type(request):
    important_date_type = ImportantDateType()
    important_date_type.author = request.user
    serializer = ImportantDateTypeSerializer(important_date_type, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(ALREADY_ADDED_RESPONSE, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_important_date_types(request):
    types_user_has_created = ImportantDateType.objects.all().filter(author=request.user)
    built_in_types = ImportantDateType.objects.all().filter(author__isnull=True)
    types = types_user_has_created.union(built_in_types)
    serializer = ImportantDateTypeSerializer(types, many=True)
    return Response(serializer.data)


# ----------------------------------------- IMPORTANT DATE TYPE -----------------------------------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_important_date(request, contact_id):
    user = request.user

    contact = get_object_or_404(Contact, id=contact_id)
    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    # try to link important date to relevant label
    if 'important_date_type' not in request.data:
        return Response({'errors': {'important_date_type': ['Label is required.']}}, status=400)
    important_date_type = ImportantDateType.objects.get(label=request.data['important_date_type'])

    important_date = ImportantDate(contact=contact, important_date_type=important_date_type)
    serializer = ImportantDateSerializer(important_date, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(ALREADY_ADDED_RESPONSE, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_important_dates(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    important_dates = list(ImportantDate.objects.all().filter(contact_id=contact))
    serializer = ImportantDateSerializer(important_dates, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_important_date(request, important_date_id):
    user = request.user
    important_date = get_object_or_404(ImportantDate, id=important_date_id)
    print('herhe')

    if str(important_date.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    operation = important_date.delete()
    if operation:
        return Response({'response': 'success'})
    return Response({'response': 'unsuccessful'}, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_important_date(request, important_date_id):
    user = request.user
    important_date = get_object_or_404(ImportantDate, id=important_date_id)

    if str(important_date.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE, status=403)

    serializer = ImportantDateSerializer(important_date, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'response': 'success'})
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


def calc_days_until_imp_date(imp_date):
    # check to see how far away an important date is
    if isinstance(imp_date, type(None)):
        return False

    today = date.today()

    # decide whether important date should be shown for this window, find days until
    delta = imp_date - today
    return delta.days


class ApiImpDateCountdown(ListAPIView):

    def get_queryset(self):
        user = self.request.user
        days_window = self.kwargs['days_window']
        within_window = []

        # goes through all contacts and checks if they are overdue
        for contact in Contact.objects.all():
            imp_dates = ImportantDate.objects.all().filter(contact=contact)
            for imp_date in imp_dates:
                days_until = calc_days_until_imp_date(imp_date.date)
                if str(contact.author) == str(user.email) and days_window > days_until >= 0:
                    within_window.append(imp_date)
        return within_window

    queryset = Contact.objects.all()
    serializer_class = ImportantDateOutSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (OrderingFilter, )











