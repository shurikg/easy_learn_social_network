from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('show-files/', views.show_files, name='show_files'),
    path('add-file/', views.add_new_file, name='add_file'),
    path('download-file/', views.download_file, name='download_file'),
    url(r'^download-file/(?P<file_id>\d+)/$', views.download_file, name='download_file'),
]
