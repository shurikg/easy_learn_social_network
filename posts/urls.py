from django.urls import path
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('home/', PostListView.as_view(), name='home'),
    path('show_post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('new/', views.create_new_post, name='newPost'),
]