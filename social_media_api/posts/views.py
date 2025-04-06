from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from django.http import JsonResponse
from .serializers import PostSerializer, CommentSerializer
from rest_framework import status
from .models import Post, Comment, Like
from rest_framework import viewsets
from accounts.models import CustomUser
from rest_framework import generics
from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from notifications.models import Notification

# post creation list update delete
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(authour=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    if post.author != user:
        return Response({"error": "cannot edit post"}, status=status.HTTP_403_FORBIDDEN)
    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid:
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    if post.author != user:
        return Response({"error": "cannot delete post"}, status=status.HTTP_403_FORBIDDEN)
    serializer = PostSerializer(post, data=request.data)
    post.delete()
    return Response({"massage": "Post succesfully deleted"}, status=status.HTTP_203_NO_CONTENT)


# comment creation listing editing and deletion
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    user = request.user
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(authour=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, pk):
    user = request.user
    comment = Comment.objects.get(id=pk)
    if comment.author != user:
        return Response({"error": "cannot edit comment"}, status=status.HTTP_403_FORBIDDEN)
    serializer = CommentSerializer(Post, data=request.data)
    if serializer.is_valid:
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_comment(request, pk):
    user = request.user
    comment = Comment.objects.get(id=pk)
    if comment.author != user:
        return Response({"error": "cannot delete comment"}, status=status.HTTP_403_FORBIDDEN)
    serializer = CommentSerializer(Post, data=request.data)
    comment.delete()
    return Response({"message": "Comment succesfully deleted"}, status=status.HTTP_203_NO_CONTENT)


class FeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        data = [
            {
                "user": post.user.username,
                "content": post.content,
                "created_at": post.created_at.isoformat()
            }
            for post in posts
        ]
        return JsonResponse({"feed": data})


class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.id
            )
        return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            return Response({'detail': 'Post unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'detail': 'Not liked yet'}, status=status.HTTP_400_BAD_REQUEST)
# dummy code
# class MethodViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]
    
#     @action(detail=False, methods=['get'], url_path='method-path')
#     def list(self, request):
#         # your code here
#         pass