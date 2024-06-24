from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import edit_profile  # edit_profile 뷰를 import  #재웅
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),  # 지현 (accounts 앱의 URL 패턴 포함)
    path('', views.home, name='home'),  # 지현

    path('accounts/edit-profile/', edit_profile, name='edit_profile'),  # 재웅
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),

    path('product/', include('products.urls', namespace='product')),  # 정현
    path('reviews/', include('reviews.urls')),  # 회성


    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?:.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]