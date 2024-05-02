from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/category/{self.slug}/'
    

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL, blank=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)   #질문 거리 image 필드 이미지 안넣으면 현재는 상품 생성 안됨.
    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품'

    def get_absolute_url(self):
        return f'/product/{self.pk}/'
# table 생성 default 이름 : customer_cart
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    