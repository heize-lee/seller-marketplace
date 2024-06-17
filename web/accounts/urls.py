# from django.urls import path, include

# urlpatterns = [
#     path('', include('allauth.urls')),
# ]

from django.urls import path, include
from .views import CustomSignupView, CustomLoginView
from . import views

urlpatterns = [
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('', include('allauth.urls')),  # Allauth의 기본 URL 포함
    path('mypage/', views.mypage_nav, name='mypage_nav'),
    path('mypage/<str:section>/', views.mypage_section, name='mypage_section'),
]