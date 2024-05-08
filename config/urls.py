from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf.urls.static import static
from django.conf import settings
from seller_product.views import ProductList, ProductCreate

urlpatterns = [
    path('order/', include('order.urls')),
    path('product/', include('seller_product.urls', namespace='product')),
    path('admin/', admin.site.urls),
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('accounts/', include('accounts.urls')),
    path('', views.home_view, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

