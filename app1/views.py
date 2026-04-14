from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'app1/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']   # ✅ FIXED

# User specific posts
class UserPostListView(ListView):
    model = Post
    template_name = 'app1/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')  # ✅ FIXED

# Single post detail
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app1/post_detail.html'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# About page
def about(request):
    return render(request, 'app1/about.html', {'title': 'About'})

# Create post (simple)
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        Post.objects.create(title=title, content=content)
        return redirect('blog-home')

    return render(request, 'blog/create_post.html')