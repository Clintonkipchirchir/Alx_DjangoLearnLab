from rest_framework import serializers

# Returns current user model(for custom user model)
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password']

        def create(self, validate_data):
            username = validate_data["username"]           
            email = validate_data["email"]   
            password = validate_data["password"]   

            user = get_user_model()
            new_user = user.objects.create_user(email=email, username=username)
            new_user.set_password(password)
            new_user.save()
            return new_user