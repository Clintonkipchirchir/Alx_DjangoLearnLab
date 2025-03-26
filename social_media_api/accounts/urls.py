from django.urls import path
from .views import register_user
from . import views
app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_user, name='register'),
]