from django.urls import path
from . import views
#from products.views import ProductListByUser, ProductUpdateView, ProductDeleteView, ProductList
from products.views import ProductList

app_name = 'product'

urlpatterns = [
    path('', views.ProductList.as_view(), name='product'), #판매 상품 리스트 페이지
    path('create/', views.ProductCreate.as_view(), name='product_create'), #제품 등록 페이지
    path('<int:pk>/', views.ProductDetail.as_view(), name='product_detail'), #상품 상세 페이지
    

    #리뷰url(회성)
    path('review/',views.review, name='review')
]