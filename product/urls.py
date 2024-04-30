
from django.urls import path ,include
from . import views
urlpatterns = [
    path('product/<int:pk>/',views.ProductDetail.as_view()),
    path('', views.ProductList.as_view()),
    path('category/<str:slug>/',views.category_page)
]
