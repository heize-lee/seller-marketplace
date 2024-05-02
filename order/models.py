from django.db import models
from django.contrib.auth.models import User
from seller_product.models import Product
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_date = models.DateField()
    payment_date = models.DateField()
    pay_confirm = models.BooleanField()