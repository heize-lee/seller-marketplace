from django.db import models

class Category(models.Model):
    category_id = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품'

