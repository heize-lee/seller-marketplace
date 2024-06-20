from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('follow/', views.follow_user, name='follow_user'),
    
    path('profile/<int:id>/', views.profile_view, name='profile_view'),
    # 기타 패턴들
]

# follow 앱의 urls.py 파일 예시

from django.urls import path
from . import views

urlpatterns = [
    path('follow/', views.follow_user, name='follow_user'),  # 이 부분이 올바르게 설정되어야 합니다.
]

