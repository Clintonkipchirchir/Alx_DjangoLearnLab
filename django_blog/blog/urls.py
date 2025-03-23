from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from .views import CommentDetailView, CommentCreateView, CommentUpdateView, CommentDeleteView
from .views import tagged_posts, search_posts
app_name = 'blog'

urlpatterns = [
    path('',PostListView.as_view(), name="blog-home"),
    path('post/tag/<str:tag_name>/', tagged_posts, name='tagged_posts'),
    path('post/search/', search_posts, name='search_posts'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.registration, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="blog/login.html", authentication_form=LoginForm), name='login'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comments/new/', CommentDetailView.as_view(), name='comment-detail'),
    path('post/<int:post_id>/comment/<int:pk>/new/', CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:post_id>/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('post/<int:post_id>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

]

