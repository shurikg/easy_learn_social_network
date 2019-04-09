from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_posts, name='home'),
    path('new/', views.create_new_post, name='newPost'),
]