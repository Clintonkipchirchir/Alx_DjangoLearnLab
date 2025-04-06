from django.urls import path
from . import views
from .views import FeedView,LikePostView, UnlikePostView


app_name = 'posts'

urlpatterns = [
    path('create_post/' ,views.create_post, name='create_post'),
    path('post_list/' ,views.post_list, name='post_list'),
    path('edit_post/<int:pk>/' ,views.update_post, name='edit_post'),
    path('delete_post/<int:pk>/' ,views.delete_post, name='delete_post'),
    path('create_comment/' ,views.create_comment, name='create_comment'),
    path('comment_list/' ,views.comment_list, name='comment_list'),
    path('edit_comment/<int:pk>/' ,views.update_comment, name='edit_comment'),
    path('delete_comment/<int:pk>/' ,views.delete_comment, name='delete_comment'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='post-unlike'),
]

