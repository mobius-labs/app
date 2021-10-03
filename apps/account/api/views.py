from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.account.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token


# Create your views here.

@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}

    if serializer.is_valid():
        user = serializer.save()
        data['response'] = "registration_successful"
        data['email'] = user.email
        token = Token.objects.get(user=user).key
        data['token'] = token
    else:
        data = serializer.errors
        return Response({'errors': data}, status=400)

    return Response(data)
