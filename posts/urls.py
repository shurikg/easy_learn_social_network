from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('show_post/<int:pk>/', login_required(PostDetailView.as_view()), name='post-detail'),
    path('feed/', login_required(PostListView.as_view()), name='feed'),
    path('new/', views.create_new_post, name='newPost'),
]