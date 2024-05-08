from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from seller_product.models import Product, Cart
# Create your models here.

class Order(models.Model):
    # settings에 있는 user_model 참조
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # product앱에 있는 Product 참조
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    total_price = models.IntegerField(default=0)
    payment_total_price = models.IntegerField(default=0)    
    amount = models.SmallIntegerField(default=0)
    order_date = models.DateField()
    payment_date = models.DateField()
    pay_confirm = models.BooleanField()

    # def save(self, *args, **kwargs):
    #     # Order를 저장할 때 Cart의 amount 값을 가져와서 Order의 amount 값으로 설정
    #     self.amount = self.cart.amount if self.cart else 0
    #     super().save(*args, **kwargs)