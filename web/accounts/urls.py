from django.urls import path, include

from .views import edit_profile   #추가


urlpatterns = [
    path('', include('allauth.urls')),
    path('edit-profile/', edit_profile, name='edit_profile'),

]