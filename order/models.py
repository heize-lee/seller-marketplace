from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from seller_product.models import Product
# Create your models here.

class Order(models.Model):
    # settings에 있는 user_model 참조
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # product앱에 있는 Product 참조
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_date = models.DateField()
    payment_date = models.DateField()
    pay_confirm = models.BooleanField()