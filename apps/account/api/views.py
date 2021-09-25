from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.account.api.serializers import RegistrationSerializer


# Create your views here.
#  takes a web request and returns a web response ;views contain logic o bdg fdxponxd


@api_view(['POST'])
def registration_view(request):
    # post: sends a body into the api, e.g. here is my username and password I want something back
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "registration_successful"
            data['email'] = user.email
        else:
            data = serializer.errors
            return Response({'errors': data}, status=400)

        return Response(data)
