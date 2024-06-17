# web/cart/urls.py

from django.urls import path
from .views import cart, cart_delete

app_name = 'cart'
urlpatterns = [
    path('', cart, name='cart'),
    path('cart_delete/<int:pk>/', cart_delete, name='cart_delete'),
    
]
