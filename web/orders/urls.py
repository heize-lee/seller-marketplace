# orders/urls.py

from django.urls import path
from .views import orders, orders_cart_delete, order_done,set_default_delivery
from django.conf import settings
from django.conf.urls.static import static

from .views import orders, orders_cart_delete, order_done
from .views import order_list
from . import views

app_name = 'orders'

urlpatterns = [
    path('', orders, name='orders'),
    path('order_cart_delete/<int:pk>/', orders_cart_delete, name='order_cart_delete'),
    path('order_done/', order_done, name='order_done'),
    path('set-default-delivery/', set_default_delivery, name='set_default_delivery'),
    path('list/', order_list, name='order_list'), # 지현
    path('mypage/orders/', views.mypage_section, {'section': 'orders'}, name='mypage_order_list'),  # 지현
]
