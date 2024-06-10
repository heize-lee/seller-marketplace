from django.urls import path
from . import views
#from products.views import ProductListByUser, ProductUpdateView, ProductDeleteView, ProductList

app_name = 'product'

urlpatterns = [
    path('create/', views.ProductCreate.as_view(), name='product_create'), #제품 등록 페이지
]