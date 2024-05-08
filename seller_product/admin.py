from django.contrib import admin
from .models import Product, Category,Cart, Comment

 
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price')
 
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    # prepopulated_fields = {'slug' : ('name',)}
 
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)

admin.site.register(Comment)





    
