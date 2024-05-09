from django.db import models
from django.conf import settings
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

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
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    quantity = models.PositiveIntegerField()   #물건 재고 수량
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=get_default_category_id)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)   #질문 거리 image 필드 이미지 안넣으면 현재는 상품 생성 안됨.
    seller_email = models.EmailField(null=True)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품'

    #  def get_absolute_url(self):
        # return f'/product/{self.pk}/'

# table 생성 default 이름 : customer_cart
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # product에 있으면 다른 유저가 담을 때 마다 total_price가 바뀜
    total_price = models.BigIntegerField(default=0)
    amount = models.IntegerField(default=0)
    payment_total_price=models.IntegerField(default=0)



