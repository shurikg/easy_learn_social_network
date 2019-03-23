from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegisterFormWizard.as_view(), name='register-wizard'),
]
