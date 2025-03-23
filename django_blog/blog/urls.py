from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView


app_name = 'blog'

urlpatterns = [
    path('',PostListView.as_view(), name="blog-home"),
    path('profile/', views.profile, name='profile'),
    path('register/', views.registration, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="blog/login.html", authentication_form=LoginForm), name='login'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),


]

