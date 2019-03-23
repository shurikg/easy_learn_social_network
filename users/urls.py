from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.RegisterFormWizard.as_view(), name='register-wizard'),
    # url('login/', views.login_page, name='login'),
    url('profile/', views.profile, name='home'),
    url('home/', views.home_page, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login')
    # url('', views.home_page, name='home'),
]
