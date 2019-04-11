from django.urls import path
from . import views
from .views import PostListView

urlpatterns = [
    path('feed/', views.home_posts, name='feed'),
    path('new/', views.create_new_post, name='newPost'),
]