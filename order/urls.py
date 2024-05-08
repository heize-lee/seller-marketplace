from django.urls import path,include
from . import views

app_name='order'
urlpatterns = [
    path('', views.order, name='order'),    
    path('password_confirm/', views.password_confirm, name='password_confirm'),    
    path('order_done/', views.order_done, name='order_done'),    
    path('order_detail/<int:pk>/', views.order_detail, name='order_detail'),    
    path('order_list/', views.order_list, name='order_list'),    
]
