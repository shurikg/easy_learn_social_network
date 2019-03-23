from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterFormWizard.as_view(), name='register-wizard'),
]
