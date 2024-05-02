
# accounts/urls.py
# Version: 1.3
# Date: 2024-04-30

# accounts/templates/accounts

# contrib
from django.urls import path, include

# register/register_done
from . import views

# account_settings
from .views import account_settings

app_name = 'accounts'

urlpatterns = [
    path('register/', views.signup_view, name='register'),  # 회원가입을 처리할 URL 패턴 설정
    path('register_done/', views.signup_done_view, name='register_done'),  # 회원가입 완료를 처리할 URL 패턴 설정

    path('settings/', account_settings, name='account_settings'),  # account_settings

    path('', include('django.contrib.auth.urls')),
]