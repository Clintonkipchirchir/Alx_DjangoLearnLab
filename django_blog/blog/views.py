from django.shortcuts import render, redirect

from .models import Post
from .forms import RegisterForm, LoginForm

def profile(request):
    posts = Post.object.all()
    return render(request, 'blog/profile.html',{
        'posts': posts
    })

    

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

def logout(request):
    return render(request, 'blog/logout.html')