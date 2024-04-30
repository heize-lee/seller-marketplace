# accounts/urls.py
# Version: 1.2
# Date: 2024-04-30

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # accounts 앱의 URL 설정을 포함
]