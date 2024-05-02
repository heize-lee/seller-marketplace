from django.contrib import admin
from .models import Product, Category

 
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price')
 
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name',)
 
admin.site.register(Category, CategoryAdmin)