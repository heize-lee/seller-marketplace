# web/review/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'reviews'
urlpatterns = [
    path('create/', views.ReviewCreate, name='create'),
    path('delete/<int:review_id>/',views.delete_review, name='delete_review'),
    path('update/<int:review_id>/',views.put_review, name='update'),
    path('review_list/<str:section>/',views.review_list,name='review_list')
    # path('check/',views.review_create_from, name='check'),
    # path('create/<int:order_id>', views.ReviewCreate, name='create'),
]
