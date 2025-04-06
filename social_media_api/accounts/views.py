from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 

from .serializers import UserSerializer, ProfileSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.http import JsonResponse


User = get_user_model()
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

# login user 
@api_view(['POST'])
def login_user(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid details"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

# profile view
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profileview(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(self.get_queryset(), id=user_id)
        user = request.user

        if user == user_to_follow:
            return JsonResponse({"error": "You cannot follow yourself."}, status=400)

        user.following.add(user_to_follow)
        user_to_follow.followers.add(user)

        return JsonResponse({"message": f"Now following {user_to_follow.username}"})

class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(self.get_queryset(), id=user_id)
        user = request.user

        if user == user_to_unfollow:
            return JsonResponse({"error": "You cannot unfollow yourself."}, status=400)

        user.following.remove(user_to_unfollow)
        user_to_unfollow.followers.remove(user)

        return JsonResponse({"message": f"Unfollowed {user_to_unfollow.username}"})
