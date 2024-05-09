from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
from order.models import Order
from seller_product.models import Product,Cart
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def home_view(request):
    products = Product.objects.all()
    context = {
        'object_list' : products
    }
    return render(request,'home.html',context)
