# web/cart/urls.py

from django.urls import path
from .views import cart, cart_delete,add_cart,plus_cart,minus_cart

app_name = 'cart'
urlpatterns = [
    path('', cart, name='cart'),
    path('cart_delete/<int:pk>/', cart_delete, name='cart_delete'),
    path('add_cart/<int:product_id>/',add_cart,name='add_cart'),
    path('plus-cart-item/',plus_cart, name='plus_cart'),
    path('minus-cart-item/',minus_cart,name='minus_cart')
]
