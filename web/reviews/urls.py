# web/review/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'reviews'
urlpatterns = [
    path('create/', views.ReviewCreate, name='create'),
    # path('create/<int:order_id>', views.ReviewCreate, name='create'),
]
