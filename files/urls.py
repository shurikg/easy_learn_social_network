from django.urls import path
from . import views

urlpatterns = [
    path('show-files/', views.show_files, name='show_files'),
    path('add-file/', views.add_new_file, name='add_file'),
]
