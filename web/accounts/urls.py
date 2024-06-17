# 지현
from django.urls import path, include
from .views import CustomSignupView, CustomLoginView
from . import views

# 재웅
from .views import edit_profile

urlpatterns = [
    # 지현
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('', include('allauth.urls')), 
    path('mypage/', views.mypage_nav, name='mypage_nav'),
    path('mypage/<str:section>/', views.mypage_section, name='mypage_section'),

    # 재웅
    path('edit-profile/', edit_profile, name='edit_profile'),
]