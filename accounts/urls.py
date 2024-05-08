
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
from seller_product.views import ProductCreate, ProductUpdateView, ProductDeleteView # SELLER

# delete_account
from .views import delete_account

app_name = 'accounts'

urlpatterns = [
    path('register/', views.signup_view, name='register'),  # 회원가입을 처리할 URL 패턴 설정
    path('register_done/', views.signup_done_view, name='register_done'),  # 회원가입 완료를 처리할 URL 패턴 설정

    path('settings/', account_settings, name='account_settings'),  # account_settings

    path('password_change/', views.password_change, name='password_change'),

    path('delete_account/', views.delete_account, name='delete_account'),
    path('delete_account_done/', views.delete_account_done, name='delete_account_done'),

    path('product/create/', ProductCreate.as_view(), name='accounts_product_create'),  # product_create
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    
    path('', include('django.contrib.auth.urls')),
]