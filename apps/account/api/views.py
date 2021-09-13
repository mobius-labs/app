from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.account.api.serializers import RegistrationSerializer

# Create your views here.

@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.date)
        data = {}

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "user registration successful"
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.error

        return Response(data)


