# config/urls.py
# Version: 1.2
# Date: 2024-04-30

from django.contrib import admin
from django.urls import include, path
from accounts import views

# profile_picture
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # accounts 앱의 URL 설정을 포함
    path('', views.home_view, name='home'),  # 루트 URL에 home_view를 연결합니다.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # profile_picture