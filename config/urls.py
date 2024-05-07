# config/urls.py
# Version: 1.2
# Date: 2024-04-30

from django.contrib import admin
from django.urls import path,include
from seller_product.views import ProductList, ProductCreate, ProductDetail
from accounts import views
# profile_picture
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('order/', include('order.urls')),

# merge-mhs 확인***

    path('product/', include('seller_product.urls', namespace='product')),

    path('admin/', admin.site.urls),
    
    path('accounts/', include('accounts.urls')),  # accounts 앱의 URL 설정을 포함
    path('', views.home_view, name='home'),  # 루트 URL에 home_view를 연결합니다.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # profile_picture



