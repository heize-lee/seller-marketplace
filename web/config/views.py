from random import sample
from django.shortcuts import render
from products.models import Category, Product  

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()  
    
  
    random_products = sample(list(products), min(len(products), 9))
    
    context = {
        'categories': categories,
        'random_products': random_products  
    }
    
    return render(request, 'home.html', context)