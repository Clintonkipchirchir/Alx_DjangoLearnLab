from rest_framework import serializers
from rest_framework.authtoken.models import Token


# Returns current user model(for custom user model)
from django.contrib.auth import get_user_model

# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password']

        def create(self, validate_data):
            user = get_user_model().objects.create_user(
                username = validate_data["username"],           
                email = validate_data["email"],   
                password = validate_data["password"],   
            )
            token = Token.objects.create(user=user)
            new_user = user.objects.create_user(email=email, username=username)
            new_user.set_password(password)
            new_user.save()
            return new_user

# login user serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=username, email=email, password=password)
        if user and user.is_active:
            token, created = Token.objects.get_or_create(user=user)


# profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'profiel_picture', 'followers']