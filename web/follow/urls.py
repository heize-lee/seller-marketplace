from django.urls import path
from .views import follow_user


urlpatterns = [
    #path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('follow/', follow_user, name='follow_user'),
    #path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    #path('profile/<int:id>/', views.profile_view, name='profile_view'),
    # 기타 패턴들
]

# follow 앱의 urls.py 파일 예시

