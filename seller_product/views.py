from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView, CreateView
from .models import Product, Category, Cart
from .forms import RegisterForm
from django.views.generic import DetailView
from .models import Product


@login_required
def modify_cart(request):
    if request.method == 'POST':
        user = request.user
        Cart.objects.filter(user=user).delete()
        product_id = request.POST['product']
        product = Product.objects.get(pk=product_id)
        cart, _ = Cart.objects.get_or_create(user=user, product=product)    
        cart.amount = int(request.POST['count'])
        if cart.amount > 0:
            cart.total_price = cart.amount * product.price
            cart.save()
        return redirect('/order/')
    else:
        return redirect('home')

class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'

class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'  # 이 부분은 적절한 템플릿 파일명으로 수정하세요.
    context_object_name = 'product'

def category_page(request, slug):  
    category = Category.objects.get(slug=slug)
    product_list = Product.objects.filter(category=category)

    return render(
        request,
        'product.html',
        {
            'product_list': product_list,
            'categories': Category.objects.all(),
            'category': category
        }
    )

class ProductCreate(CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'category']
    template_name = 'product_create.html'
    success_url = '/product/'  # 적절한 URL로 수정하세요.
