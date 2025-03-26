from rest_framework import serializers
from rest_framework.authtoken.models import Token


# Returns current user model(for custom user model)
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password']

        def create(self, validate_data):
            user = get_usermodel().objects.create_user(
                username = validate_data["username"],           
                email = validate_data["email"],   
                password = validate_data["password"],   
            )
            token = Token.objects.create(user=user)
            new_user = user.objects.create_user(email=email, username=username)
            new_user.set_password(password)
            new_user.save()
            return new_user