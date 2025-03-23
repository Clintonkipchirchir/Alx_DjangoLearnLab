from django.shortcuts import render, redirect

from .models import Post
from .forms import RegisterForm, LoginForm

def profile(request):
    posts = Post.object.all()
    pass

    

def registration(request):
     if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/login/')
     else:
        form = RegisterForm()

     return render(request, 'blog/registration.html', {
        'form': form
    })

def profile*()