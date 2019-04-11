from django.shortcuts import render, redirect
from .forms import NewPost, Comment
from .models import Post
from django.views.generic import ListView
from users.models import Profile


def home_posts(request):
    other_posts = Post.objects.filter(category="other")
    user = Profile.objects.get(user=request.user)
    context = {
        'posts': Post.objects.all(), 'study_posts': Post.objects.filter(category="other")
    }
    return render(request, 'posts/Feed.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'posts/Feed.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date']


def create_new_post(request):
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:home')
    form = NewPost
    return render(request, 'posts/new_post.html', {"form": form})