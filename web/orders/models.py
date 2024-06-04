from django.db import models
# from products.models import Product
from django.conf import settings
# 카트 모델 고민

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    # cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    
    # 카트에 있는 데이터가 지워지면 참조가 안됨
    # 카트 컬럼과 같은 이름으로 데이터 저장
    amount = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    payment_total_price = models.IntegerField(default=0)    

    order_date = models.DateField()
    # payment앱에 추가예정
    # payment_date = models.DateField()
    # pay_confirm = models.BooleanField()
    
    def save(self, *args, **kwargs):
        # Cart에서 같은 데이터 가져와서 Order의 각 컬럼에 할당
        if self.cart:
            self.amount = self.cart.amount
            self.total_price = self.cart.total_price
            self.payment_total_price = self.cart.payment_total_price
        super().save(*args, **kwargs)
        
