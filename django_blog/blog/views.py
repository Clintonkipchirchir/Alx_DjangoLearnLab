from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

class PostDetailView(DetailView):
    model = Post

class PostListView(ListView):
  model = Post
  context_object_name = 'posts'
  ordering = ["-date_posted"]


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title',
        'content',
        ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# update view
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = [
        'title',
        'content',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else: return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
      post = self.get_object()
      if self.request.user == post.author:
          return True
      else: return False
