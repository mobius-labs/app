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
        )
        password = self.validated_data['password']

        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            # we use "confirm_password" so the error message
            # appears below the confirm_password field in the UI
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['business_card', 'email', 'connected_contact', 'business_card_theme']
        read_only_fields = ['email']
