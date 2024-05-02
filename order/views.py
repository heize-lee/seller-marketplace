from django.shortcuts import render,redirect

from .models import Order
from seller_product.models import Product
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.
def order(request):    
    product = Product.objects.all()
    # product_id = request.GET['product_id']
    # product = Product.objects.get(pk=product_id)
    # 이전에 해당 상품에 대한 장바구니 정보가 있으면 get(product=product)
    # 없으면 새로 생성해서 적용
    # try:
    #     order = Product.objects.get(product=product) # get(user=request.user,
    # except:
    #     order = product.objects.create(product=product) # create(user=request.user, quantity=0,
    # finally:
    #     pass
    # product.quantity+=1
    # product.save()
    context = {
        'object': product
    }
    return render(request, template_name='order/order_detail.html', context=context)

def order_done(request):
    product = Product.objects.all()
    context = {
        'object': product
    }
    return render(request,'order/order_done.html')