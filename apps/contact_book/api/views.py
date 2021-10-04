from django.db import IntegrityError
from django.db.models import Model
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from apps.contact_book.api.serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.contact_book.models import *


NOT_PERMITTED_RESPONSE = {'has_permissions': False}

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_contact_by_id(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

    serializer = ContactSerializer(contact)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_contacts(request):
    user = request.user
    contacts = Contact.objects.all()
    accessible_contacts = []

    for contact in contacts:
        if str(contact.author) == str(user.email):
            accessible_contacts.append(contact)

    serializer = ContactSerializer(accessible_contacts, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_contact_by_id(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

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
        return Response(NOT_PERMITTED_RESPONSE)

    serializer = ContactSerializer(contact, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'response': 'success'})
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


# ---------------------------------------- PHONE NUMBERS ----------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_phone_no(request, contact_id):
    user = request.user

    # firstly check if the contact exists, and the contact was created by the author
    contact = get_object_or_404(Contact, id=contact_id)
    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

    # then created the phone number
    phone_no = Number(contact=contact)
    serializer = NumberSerializer(phone_no, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'response': 'already_added'}, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phone_nos_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

    numbers = get_list_or_404(Number, contact_id=contact)
    serializer = NumberSerializer(numbers, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_phone_no_by_pid(request, number_id):
    user = request.user
    number = get_object_or_404(Number, id=number_id)

    if str(number.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

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
        return Response(NOT_PERMITTED_RESPONSE)

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
        return Response(NOT_PERMITTED_RESPONSE)

    address = Address(contact=contact)
    serializer = AddressSerializer(address, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'response': 'already_added'}, status=400)
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_addresses_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

    addresses = get_list_or_404(Address, contact_id=contact)
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_address_by_aid(request, address_id):
    user = request.user
    address = get_object_or_404(Address, id=address_id)

    if str(address.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

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
        return Response(NOT_PERMITTED_RESPONSE)

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
        return Response(NOT_PERMITTED_RESPONSE)

    email = Email(contact=contact)
    serializer = EmailSerializer(email, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'entry already added'})

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_emails_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

    emails = get_list_or_404(Email, contact_id=contact)
    serializer = EmailSerializer(emails, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_email_by_eid(request, email_id):
    user = request.user
    email = get_object_or_404(Email, id=email_id)

    if str(email.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

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
        return Response(NOT_PERMITTED_RESPONSE)

    serializer = EmailSerializer(email, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'response': 'success'})
        except IntegrityError:
            return Response({'entry already added'})

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


# ----------------------------------------- SOCIAL MEDIA SITE -----------------------------------------


@api_view(['POST'])
def create_social_media_site(request):
    social_media_site = SocialMediaSite()
    serializer = SocialMediaSiteSerializer(social_media_site, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'entry already added'}, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


'''
@api_view(['GET'])
def get_social_media_site(request, site):
    
    social_media_site = get_object_or_404(SocialMediaSite, site=site)
    serializer = SocialMediaSiteSerializer(social_media_site)
    return Response(serializer.data)
'''


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_social_media_sites(request):
    social_media_site = get_list_or_404(SocialMediaSite, is_default=True)
    serializer = SocialMediaSiteSerializer(social_media_site, many=True)
    return Response(serializer.data)


# ----------------------------------------- SOCIAL MEDIA -----------------------------------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_social_media_contact(request, contact_id):
    user = request.user

    contact = get_object_or_404(Contact, id=contact_id)
    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

    # try to link social media link to relevant site - create new site if not already in db
    try:
        social_media_site = SocialMediaSite.objects.get(site=request.data.__getitem__('site'))

    except SocialMediaSite.DoesNotExist:
        # could put this into its own function.
        social_media_site = SocialMediaSite()
        serializer = SocialMediaSiteSerializer(social_media_site, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            data = serializer.errors
            return Response({'errors': data}, status=400)

        social_media_site = SocialMediaSite.objects.get(site=request.data.__getitem__('site'))

    social_media_contact = SocialMediaContact(contact=contact, social_media_site=social_media_site)
    serializer = SocialMediaContactSerializer(social_media_contact, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'entry already added'}, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_socials_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

    socials = get_list_or_404(SocialMediaContact, contact_id=contact)
    serializer = SocialMediaContactOutSerializer(socials, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_social_by_sid(request, social_media_contact_id):
    user = request.user
    social_media_contact = get_object_or_404(SocialMediaContact, id=social_media_contact_id)

    if str(social_media_contact.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

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
        return Response(NOT_PERMITTED_RESPONSE)

    serializer = SocialMediaContactSerializer(social_media_contact, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'response': 'success'})
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


# ----------------------------------------- IMPORTANT DATE TYPE -----------------------------------------


@api_view(['POST'])
def create_important_date_type(request):
    important_date_type = ImportantDateType()
    serializer = ImportantDateTypeSerializer(important_date_type, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'entry already added'}, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_important_date_types(request):
    important_date_type = get_list_or_404(ImportantDateType, is_default=True)
    serializer = ImportantDateTypeSerializer(important_date_type, many=True)
    return Response(serializer.data)


# ----------------------------------------- IMPORTANT DATE TYPE -----------------------------------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_important_date(request, contact_id):
    user = request.user

    contact = get_object_or_404(Contact, id=contact_id)
    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

    # try to link important date to relevant label - create new label if not already in db
    try:
        important_date_type = ImportantDateType.objects.get(label=request.data.__getitem__('label'))

    except ImportantDateType.DoesNotExist:
        # could put this into its own function.
        important_date_type = ImportantDateType()
        serializer = ImportantDateTypeSerializer(important_date_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            data = serializer.errors
            return Response({'errors': data}, status=400)

        important_date_type = ImportantDateType.objects.get(label=request.data.__getitem__('label'))

    important_date = ImportantDate(contact=contact, important_date_type=important_date_type)
    serializer = ImportantDateSerializer(important_date, data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'entry already added'}, status=400)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_important_dates(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

    important_dates = get_list_or_404(ImportantDate, contact_id=contact)
    serializer = ImportantDateOutSerializer(important_dates, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_important_date(request, important_date_id):
    user = request.user
    important_date = get_object_or_404(ImportantDate, id=important_date_id)
    print('herhe')

    if str(important_date.contact.author) != str(user.email):
        return Response(NOT_PERMITTED_RESPONSE)

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
        return Response(NOT_PERMITTED_RESPONSE)

    serializer = ImportantDateSerializer(important_date, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'response': 'success'})
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)
