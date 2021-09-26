from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from apps.contact_book.models import *
from apps.contact_book.api.serializers import ContactSerializer

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def get_contact_view(request, contact_id):

    try:
        contact = Contact.objects.get(contact_id)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ContactSerializer(contact)
        return Response(serializer.data)


@api_view(['POST'])
def create_contact_view(request):

    if request.method == 'POST':
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



