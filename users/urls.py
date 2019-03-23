from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.RegisterFormWizard.as_view(), name='register-wizard'),
    # url('login/', views.login_page, name='login'),
    url('profile/', views.profile, name='profile'),
    path('profile-shlomi/', views.view_profile, name='view_profile'),
    url('home/', views.home_page, name='home'),
    path('home-shlomi/', views.home, name='home-shlomi'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # url('', views.home_page, name='home'),
    path('', views.RegisterFormWizard.as_view(), name='register-wizard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit/personal-info/', views.edit_personal_info, name='edit_personal_info'),
    path('profile/edit/more-info/', views.edit_more_info, name='edit_more_info'),
    path('profile/edit/change-password/', views.change_password, name='change_password'),
]
