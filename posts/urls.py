from django.urls import path
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('show_post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('feed/', views.home_posts, name='feed'),
    path('new/', views.create_new_post, name='newPost'),
]