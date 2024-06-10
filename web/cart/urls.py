# web/cart/urls.py

from django.urls import path
from .views import cart

urlpatterns = [
    path('', cart, name='cart'),
    
]
