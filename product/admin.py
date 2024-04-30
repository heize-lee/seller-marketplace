from django.contrib import admin
from .models import Product,Category

admin.site.register(Product)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
admin.site.register(Category,CategoryAdmin)
# Register your models here.
