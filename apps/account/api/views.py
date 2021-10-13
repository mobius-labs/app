from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from apps.account.api.serializers import RegistrationSerializer, UserSerializer
from rest_framework.authtoken.models import Token
import random
import string

'''
def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))
'''


@api_view(['POST'])
@permission_classes([])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        # user.business_card_url = get_random_string(10)
        # user.save()
        data['response'] = "user registration successful"
        data['email'] = user.email
        token = Token.objects.get(user=user).key
        data['token'] = token

    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)

    return Response(data)


@api_view(['PUT'])
@permission_classes([])
def update_business_card_visibility(request):
    calling_user = request.user

    serializer = UserSerializer(calling_user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'update successful'})
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)


@api_view(['GET'])
@permission_classes([])
def get_business_card_visibility(request):
    calling_user = request.user

    serializer = UserSerializer(calling_user)
    return Response(serializer.data)
