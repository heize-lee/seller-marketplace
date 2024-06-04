# web/orders/urls.py

from django.urls import path
from .views import orders

urlpatterns = [
    path('', orders, name='orders'),
    
]
