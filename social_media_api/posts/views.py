from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 

from .serializers import PostSerializer, CommentSerializer
from rest_framework import status
from .models import Post, Comment
from rest_framework import viewsets

# post creation list update delete
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user
    serializer = PostSerializer(data=requst.data)
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
    serializer = CommentSerializer(data=requst.data)
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
    serializer = CommentSerializer(post, data=request.data)
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
    serializer = CommentSerializer(post, data=request.data)
    comment.delete()
    return Response({"message": "Comment succesfully deleted"}, status=status.HTTP_203_NO_CONTENT)


# dummy code
# class MethodViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]
    
#     @action(detail=False, methods=['get'], url_path='method-path')
#     def list(self, request):
#         # your code here
#         pass