from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/category/{self.slug}/'
    

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품'

    def get_absolute_url(self):
        return f'/product/{self.pk}/'
