from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model




# register user
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        User = get_user_model()
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password']) #sets password as a hash password
        user.save() #saves the password as hash password
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

