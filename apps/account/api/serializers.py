from rest_framework import serializers
from apps.account.models import User


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
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        # returning a json message
        if password != confirm_password:
            serializers.ValidationError({'password': 'Passwords do no match.'})

        # if the passwords are the same
        user.set_password(password)
        user.save()
        return user
