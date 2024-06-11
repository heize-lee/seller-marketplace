from django.contrib import admin
from .models import Product, Category

 
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price')
 
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    # prepopulated_fields = {'slug' : ('name',)}
 
admin.site.register(Category, CategoryAdmin)

