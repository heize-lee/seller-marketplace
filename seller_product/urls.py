from django.urls import path
from . import views
from seller_product.views import ProductListByUser, ProductUpdateView, ProductDeleteView, ProductList

app_name = 'product'

urlpatterns = [
    # 상품 목록 페이지
    path('', views.ProductList.as_view(), name='product'),
    # 상품 상세 페이지
    path('<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('create/', views.ProductCreate.as_view(), name='product_create'),
    path('modify-cart/',views.modify_cart,name='modify_cart'),
    path('search/<str:q>/', views.ProductSearch.as_view()),

    path('my_products/', ProductListByUser.as_view(), name='my_products'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('search/<str:q>/', views.ProductSearch.as_view()),
    path('category/<str:slug>/',views.category_page),
]


