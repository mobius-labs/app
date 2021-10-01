from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from apps.contact_book.api.serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.contact_book.models import *

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
        return Response({'user does not have permission to access contact'})

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
        return Response({'user does not have permission to access contact'})

    operation = contact.delete()
    if operation:
        return Response({'delete successful'})
    return Response({'delete unsuccessful'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_contact_by_id(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response({'user does not have permission to access contact'})

    serializer = ContactSerializer(contact, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'update successful'})
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
        return Response({'user does not have permission to access contact'})

    # then created the phone number
    phone_no = Number(contact=contact)
    serializer = NumberSerializer(phone_no, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phone_nos_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response({'user does not have permission to access contact'})

    numbers = get_list_or_404(Number, contact_id=contact)
    serializer = NumberSerializer(numbers, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_phone_no_by_pid(request, number_id):
    user = request.user
    number = get_object_or_404(Number, id=number_id)

    if str(number.contact.author) != str(user.email):
        return Response({'user does not have permission to access contact'})

    operation = number.delete()
    if operation:
        return Response({'delete successful'})
    return Response({'delete unsuccessful'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_phone_no_by_pid(request, number_id):
    user = request.user
    number = get_object_or_404(Number, id=number_id)

    if str(number.contact.author) != str(user.email):
        return Response({'user does not have permission to access contact'})

    serializer = NumberSerializer(number, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'update successful'})
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
        return Response({'user does not have permission to access contact'})

    address = Address(contact=contact)
    serializer = AddressSerializer(address, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_addresses_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response({'user does not have permission to access contact'})

    addresses = get_list_or_404(Address, contact_id=contact)
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_address_by_aid(request, address_id):
    user = request.user
    address = get_object_or_404(Address, id=address_id)

    if str(address.contact.author) != str(user.email):
        return Response({'user does not have permission to access contact'})

    operation = address.delete()
    if operation:
        return Response({'delete successful'})
    return Response({'delete unsuccessful'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_address_by_aid(request, address_id):
    user = request.user
    address = get_object_or_404(Address, id=address_id)

    if str(address.contact.author) != str(user.email):
        return Response({'user does not have permission to access contact'})

    serializer = AddressSerializer(address, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'update successful'})
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
        return Response({'user does not have permission to access contact'})

    email = Email(contact=contact)
    serializer = EmailSerializer(email, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_emails_by_cid(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if str(contact.author) != str(user.email):
        return Response({'user does not have permission to access contact'})

    emails = get_list_or_404(Email, contact_id=contact)
    serializer = EmailSerializer(emails, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_email_by_eid(request, email_id):
    user = request.user
    email = get_object_or_404(Email, id=email_id)

    if str(email.contact.author) != str(user.email):
        return Response({'user does not have permission to access contact'})

    operation = email.delete()
    if operation:
        return Response({'delete successful'})
    return Response({'delete unsuccessful'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_email_by_eid(request, email_id):
    user = request.user
    email = get_object_or_404(Email, id=email_id)

    if str(email.contact.author) != str(user.email):
        return Response({'user does not have permission to access contact'})

    serializer = EmailSerializer(email, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'update successful'})
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)
