from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,Category
# Create your views here.

class ProductList(ListView):
    model = Product
    ordering = '-pk'

def category_page(request,slug):  
    category = Category.objects.get(slug=slug)
    product_list = Product.objects.filter(category=category)

    return render(
        request,
        'product/product_list.html',
        {
            'product_list': product_list,
            'categories': Category.objects.all(),
            'category':category
        }
    )

class ProductDetail(DetailView):
    model=Product
