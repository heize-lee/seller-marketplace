
# accounts/urls.py
# Version: 1.3
# Date: 2024-04-30

# accounts/templates/accounts

from django.urls import path, include
from . import views
# from django.contrib.auth.views import PasswordResetConfirmView

app_name = 'accounts'

urlpatterns = [
    
    path('register/', views.signup_view, name='register'),  # 회원가입을 처리할 URL 패턴 설정
    path('register_done/', views.signup_done_view, name='register_done'),  # 회원가입 완료를 처리할 URL 패턴 설정

    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('', include('django.contrib.auth.urls')),
]