from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from apps.contact_book.api.serializers import ContactSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.contact_book.models import Contact


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
        return Response({'user does not have permission to get id'})

    serializer = ContactSerializer(contact)
    return Response(serializer.data)