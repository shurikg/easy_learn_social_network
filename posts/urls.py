from django.urls import path
from . import views
from .views import PostListView

urlpatterns = [
    path('home/', PostListView.as_view(), name='home'),
    path('new/', views.create_new_post, name='newPost'),
]