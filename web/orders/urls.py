# orders/urls.py

from django.urls import path
from .views import orders, orders_cart_delete, order_done

app_name = 'orders'
urlpatterns = [
    path('', orders, name='orders'),
    path('order_cart_delete/<int:pk>/', orders_cart_delete, name='order_cart_delete'),
    path('order_done/', order_done, name='order_done'),
    
]
