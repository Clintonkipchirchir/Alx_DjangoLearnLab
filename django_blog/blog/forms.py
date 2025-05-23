from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.forms import TagWidget

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        }))
    
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'email@gmail.com',
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        }))

class Post(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title" ,"content" ,"published_date" ,"author", "tag"]
        widgets = {
            'tags': TagWidget(),  # This widget makes tag entry user-friendly.
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'email', 'content']  # Adjust fields as necessary
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Enter your comment here...'}),
        }
    
      