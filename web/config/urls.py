
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import edit_profile  # edit_profile 뷰를 import  #재웅

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls')),
    # path('', include('home.urls')),  # home 앱의 URL을 포함
    path('payment/', include('payment.urls')),
    path('accounts/', include('accounts.urls')),  # 지현 (accounts 앱의 URL 패턴 포함)
    path('', views.home, name='home'), # 지현

    path('product/', include('products.urls', namespace='product')), # 정현
    
    path('accounts/edit-profile/', edit_profile, name='edit_profile'),  # 재웅
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)