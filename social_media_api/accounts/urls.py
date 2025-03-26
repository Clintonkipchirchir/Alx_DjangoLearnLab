from django.urls import path
from .views import register_user, login_user
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
]