from django.urls import path
from .views import follow_user, unfollow_user


urlpatterns = [
    path('follow/', follow_user, name='follow_user'),
    path('unfollow/', unfollow_user, name='unfollow_user'),
   
]

# follow 앱의 urls.py 파일 예시

