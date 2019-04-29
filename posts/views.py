from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from files.models import File
from .models import Post, Comments
from django.views.generic import ListView, DetailView
from .forms import NewPost, Comment, OTHER_CATEGORY
from users.models import Profile, UserCourses
from django.contrib.auth.models import User


# def home_posts(request):
#     other_posts = Post.objects.filter(category="other")
#     user = Profile.objects.get(user=request.user)
#     context = {
#         'posts': Post.objects.all(), 'study_posts': Post.objects.filter(category="other")
#     }
#     return render(request, 'posts/Feed.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'posts/Feed.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 5

    def get_queryset(self):
        profile_obj = Profile.objects.get(user=self.request.user)
        friends_list = tuple(friend.user.username for friend in profile_obj.friends.all())
        all_posts = Post.objects.all()
        user_courses = tuple(course.course_id.course_name for course in UserCourses.objects.filter(user_id=profile_obj))
        posts_to_show = []
        for post in all_posts:
            if post.category == OTHER_CATEGORY and post.author.username in (friends_list + (self.request.user.username,)):
                posts_to_show.append(post)
            elif post.category in user_courses:
                posts_to_show.append(post)
        return posts_to_show


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    form_class = Comment

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = self.form_class(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = self.request.user
            new_comment.postId = self.object
            new_comment.save()
            self.form_class = Comment
        else:
            messages.error(request, f'Some error occurred while posting your comment.')
            self.form_class = comment_form
        context = self.get_context_data()
        return super(PostDetailView, self).render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        return super(PostDetailView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(postId_id=self.object).order_by('-publish_date')
        context['comment_form'] = self.form_class
        return context


@login_required
def create_new_post(request):
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:feed')
    form = NewPost
    return render(request, 'posts/new_post.html', {"form": form})

def download_file(request, file_id):
    print(file_id)
    file = File.objects.get(id=file_id)
    #files = File.objects.all()

    #file = File.objects.all()

    #file = File.objects.filter(category=category)
    args = {'file': file, }
    return render(request, 'files/download_file.html', args)