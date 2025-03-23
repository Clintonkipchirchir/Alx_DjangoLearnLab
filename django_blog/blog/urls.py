from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

app_name = 'blog'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('register/', views.registration, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="blog/log_in.html", authentication_form=LoginForm), name='login'),
]
