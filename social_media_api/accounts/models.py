from django.db import models

# import abstract user
from django.contrib.auth.models import AbstractUser

# Create custom user model with bio, profile picture and follower7s
class CustomUser(AbstractUser):
    bio =models.TextField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='follow', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers_following', blank=True)
    