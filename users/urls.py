from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit/personal-info/', views.edit_personal_info, name='edit_personal_info'),
    path('profile/edit/more-info/', views.edit_more_info, name='edit_more_info'),
    path('profile/edit/educational-info/', views.edit_educational_info, name='edit_educational_info'),

    path('profile/edit/privacy', views.edit_privacy, name='edit_privacy'),
    path('profile/edit/change-password/', views.change_password, name='change_password'),
    path('show-users/', views.show_users, name='show_users'),
    #path('show-users/selected-user/', views.show_selected_user, name='selected_user'),
    url(r'^show-users/selected-user/(?P<id>[\w-]+)/$', views.show_selected_user, name='selected_user'),
    #url(r'^(?P<slug>[\w-]+)/$', views.show_selected_user),
    path('show-users/results/', views.search_result, name='search'),
    url(r'^friend-request/send/(?P<id>[\w-]+)/$', views.send_friend_request, name='send_friend_request'),
    url(r'^friend-request/cancel/(?P<id>[\w-]+)/$', views.cancel_friend_request,name='cancel_friend_request'),
    url(r'^friend-request/accept/(?P<id>[\w-]+)/$', views.accept_friend_request, name='accept_friend_request'),
    url(r'^friend-request/delete/(?P<id>[\w-]+)/$', views.delete_friend_request, name='delete_friend_request'),
    path('friends/<int:user_id>', views.list_of_friends, name='list_of_friends'),
    path('show-users/delete-user/<int:user_id>', views.delete_friend, name='delete_friend'),

    path('rules/', views.web_rules, name='rules'),
]
