from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import RegisterForm, LoginForm

@login_required
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

@login_required
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = '__all__'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# update view
@login_required
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

@login_required
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
      post = self.get_object()
      if self.request.user == post.author:
          return True
      else: return False

class CommentDetailView(DetailView):
    model = Comment

class CommentListView(ListView):
  model = Comment
  context_object_name = 'comments'
  ordering = ["-date_posted"]

@login_required
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = "__all__"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# update view
@login_required
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = "__all__"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else: return False

@login_required
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/'

    def test_func(self):
      post = self.get_object()
      if self.request.user == post.author:
          return True
      else: return False