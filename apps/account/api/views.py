from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from apps.account.api.serializers import RegistrationSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from apps.account.models import User


@api_view(['POST'])
@permission_classes([])
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_info(request):
    serialised = UserSerializer(request.user)
    return Response(serialised.data['email'])

