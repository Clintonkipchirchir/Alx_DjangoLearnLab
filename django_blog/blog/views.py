from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Tag
from .forms import RegisterForm, LoginForm
from django.db.models import Q


def search_posts(request):
    query = request.GET.get('q', '')
    results = Post.objects.all()
    
    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'blog/search_results.html', context)

def tagged_posts(request, tag_name):
    # Filter posts where the tag name matches (case-insensitive)
    posts = Post.objects.filter(tags__name__iexact=tag_name)
    context = {
        'tag': tag_name,
        'posts': posts,
    }
    return render(request, 'posts/tagged_posts.html', context)


class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_by_tag_list.html'  # Customize your template path
    context_object_name = 'posts'
    paginate_by = 10  # Optional: paginate if you have many posts

    def get_queryset(self):
        # Extract the tag slug from URL parameters
        tag_slug = self.kwargs.get('tag_slug')
        # Filter posts based on the tag slug (case-insensitive)
        return Post.objects.filter(tags__slug__iexact=tag_slug).distinct()

    def get_context_data(self, **kwargs):
        # Add additional context to the template, e.g., the tag slug
        context = super().get_context_data(**kwargs)
        context['tag_slug'] = self.kwargs.get('tag_slug')
        return context
    
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