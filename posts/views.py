from django.shortcuts import render, redirect
from .forms import NewPost
from .models import Post
from django.views.generic import ListView


def home_posts(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'home_posts.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'home_posts.html'  # <app>/<model>_<viewtype>.html
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
    return render(request, 'new_post.html', {"form": form})




# class PostDetailView(DetailView):
#     model = Post