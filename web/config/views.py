from django.shortcuts import render
from products.models import Category, Product

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()  # 모든 상품을 가져옴
    return render(request, 'home.html', {'categories': categories, 'products': products})

