from rest_framework import serializers
from apps.account.models import User

# a serializer allows complex data such as querysets and model instances to be converted to python datatypes
# these types can be rendered to json


# Create your ModelSerializers here
class RegistrationSerializer(serializers.ModelSerializer):

    # need to create confirm password as its not from our User model
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

        # hides password field
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            #username=self.validated_data['username']
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            # returning a json message
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data
