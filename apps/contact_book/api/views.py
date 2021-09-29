from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from apps.contact_book.api.serializers import ContactSerializer
from rest_framework.decorators import api_view


@api_view(['POST'])
def create_contact_view(request):
    serializer = ContactSerializer(data=request.data)
    data = {}

    if serializer.is_valid():
        contact = serializer.save()
        data['response'] = "new contact created"
        data['first_name'] = contact.first_name
        data['surname'] = contact.surname
        data['middle_name'] = contact.middle_name
        data['nickname'] = contact.nickname
        data['name_pronunciation'] = contact.name_pronunciation
        data['pronouns'] = contact.pronouns
        data['title'] = contact.title
        data['relation'] = contact.relation
        data['company'] = contact.company
        data['job_title'] = contact.job_title
        data['side_notes'] = contact.side_notes
        data['department'] = contact.department
        data['regularity_of_contact'] = contact.regularity_of_contact



    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)

    return Response(data)

'''
@api_view(['GET'])
def get_contact_view(request, contact_id):

    try:
        contact = Contact.objects.get(contact_id)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ContactSerializer(contact)
    return Response(serializer.data)

@api_view(['POST'])
def create_contact_view(request):
    serializer = ContactSerializer(data=request.data)
    data = {}

    if serializer.is_valid():
        contact = serializer.save()
        data['response'] = "contact creation successful"
        data['email'] = contact.email

    else:
        data = serializer.errors
        return Response(data, status=400)

    return Response(data)
'''