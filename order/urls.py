from django.urls import path,include
from . import views

app_name='order'
urlpatterns = [
    path('', views.order),    
    path('order_done/', views.order_done, name='order_done'),    
    
]
