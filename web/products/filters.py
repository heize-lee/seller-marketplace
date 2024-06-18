# filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='product_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='product_price', lookup_expr='lte')
    search_keyword = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'search_keyword']
