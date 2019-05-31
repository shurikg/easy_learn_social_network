from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import url
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('show_post/<int:pk>/', login_required(PostDetailView.as_view()), name='post-detail'),
    path('feed/', login_required(PostListView.as_view()), name='feed'),
    path('new/', views.create_new_post, name='newPost'),
    url(r'^delete_post/(?P<post_id>\d+)/$', views.delete_post, name='delete_post'),
    path('delete-comment/<int:comment_id>', login_required(views.delete_comment), name='delete_comment'),
]
