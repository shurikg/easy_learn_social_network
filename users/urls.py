from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.RegisterFormWizard.as_view(), name='register-wizard'),
    path('home/', views.home, name='home'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit/personal-info/', views.edit_personal_info, name='edit_personal_info'),
    path('profile/edit/more-info/', views.edit_more_info, name='edit_more_info'),
    path('profile/edit/change-password/', views.change_password, name='change_password'),
    url(r'^register/$', views.register, name='register'),
]
