from django.db import models
# from products.models import Product
from django.conf import settings


# Create your models here.
class Cart(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # product에 있으면 다른 유저가 담을 때 마다 total_price가 바뀜
    total_price = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    payment_total_price=models.IntegerField(default=0)