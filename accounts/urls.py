
# accounts/urls.py
# Version: 1.3
# Date: 2024-04-30

# accounts/templates/accounts

from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.signup_view, name='register'),
    path('', include('django.contrib.auth.urls')),
]
