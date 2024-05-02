
from django.urls import path ,include
from . import views
app_name = 'product'
urlpatterns = [
    path('modify-cart/',views.modify_cart,name='modify_cart'),
    path('<int:pk>/',views.ProductDetail.as_view()),
    path('', views.ProductList.as_view()),
    path('category/<str:slug>/',views.category_page)
]
