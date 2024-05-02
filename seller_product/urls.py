
from django.urls import path 
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductList.as_view()),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('product/create/', views.ProductCreate.as_view(), name='product_create'),
    path('modify-cart/',views.modify_cart,name='modify_cart'),
    # path('<int:pk>/',views.ProductDetail.as_view()),
    
    
    
    # path('category/<str:slug>/',views.category_page)
]
