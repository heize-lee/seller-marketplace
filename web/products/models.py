#web/products/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # 이미지 필드 추가

    def __str__(self):
        return self.category_name
    
    # def get_absolute_url(self):
    #     return f'/category/{self.slug}/'
    
    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'



def get_default_category_id():
    first_category = Category.objects.first()  # 첫 번째 카테고리 가져오기
    if first_category:
        return first_category.pk  # 카테고리의 ID 반환
    return None

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=0)  #이름 수정됨
    description = models.TextField()
    stock_quantity = models.PositiveIntegerField()   #이름 수정됨
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=get_default_category_id)
    product_img = models.ImageField(upload_to='product_images/', null=True, blank=True)  #이름 수정됨
    seller_email = models.EmailField(null=True)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품'

    def save(self, *args, **kwargs):
        if self.pk:  # 인스턴스가 이미 존재하는 경우에만 updated_date 업데이트
            self.updated_date = timezone.now()
        super().save(*args, **kwargs)