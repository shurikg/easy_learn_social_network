from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Post, Comments
from django.views.generic import ListView, DetailView
from .forms import NewPostForm, Comment, PRIVATE_CATEGORY
from users.models import Profile, UserCourses
from files.forms import CreateNewFileForm

FLAGS = {
    'want_add_file': False
}


class PostListView(ListView):
    model = Post
    template_name = 'posts/Feed.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        posts_list = self.get_queryset()
        posts = []
        for post in posts_list:
            profile = Profile.objects.get(user=post.author)
            p = {'post': post, 'profile': profile}
            posts.append(p)
        context.update({
            'all_posts': posts,
        })
        return context

    def get_queryset(self):
        profile_obj = Profile.objects.get(user=self.request.user)
        friends_list = tuple(friend.user.username for friend in profile_obj.friends.all())
        all_posts = Post.objects.all().order_by('-date')
        user_courses = ()
        try:
            user_courses = tuple(course.course_name for course in tuple([c.course_id.all() for c in
                                                                UserCourses.objects.filter(user_id=profile_obj)][0]))
        except IndexError as e:
            print(e)
        posts_to_show = []
        for post in all_posts:
            if post.category == PRIVATE_CATEGORY and post.author.username in (friends_list + (self.request.user.username,)):
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
        post_form = NewPostForm(request.POST)
        if 'add_file' in request.POST:
            FLAGS['want_add_file'] = True
            file_form = CreateNewFileForm
            return render(request, 'posts/new_post.html', {"post_form": post_form, "file_form": file_form})
        else:
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user
                if FLAGS['want_add_file'] is True:
                    file_form = CreateNewFileForm(request.POST, request.FILES)
                    if file_form.is_valid():
                        file = file_form.save(commit=False)
                        file.owner = request.user
                        file.save()
                        file_form.save_m2m()
                        post.file = file
                        FLAGS['want_add_file'] = False
                    else:
                        error_message = file_form.errors
                        post_form = NewPostForm
                        return render(request, 'posts/new_post.html',
                                      {"post_form": post_form, "error_message": error_message})
                else:
                     post.file = None
                post.save()
                return redirect('posts:feed')
            else:
                error_message = 'Error by trying to write post!'
                post_form = NewPostForm
                return render(request, 'posts/new_post.html', {"post_form": post_form, "error_message": error_message})

    else:
        post_form = NewPostForm
        return render(request, 'posts/new_post.html', {"post_form": post_form})


@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('posts:feed')


@login_required
def delete_comment(request, comment_id):
    try:
        comment = Comments.objects.get(id=comment_id)
        post_id = comment.postId.id
        if request.user != comment.author:
            messages.error(request, 'You cannot delete comment of other user!')
            return PostDetailView.as_view()(request, pk=post_id)
        comment.delete()
        return PostDetailView.as_view()(request, pk=post_id)
    except Comments.DoesNotExist as e:
        print(e)
        return redirect('posts:feed')
