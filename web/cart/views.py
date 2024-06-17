from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from products.models import Product

# Create your views here.
def cart(request):
    # 카트페이지 처음 들어왔을 때 
    if request.method == 'GET':
        user = request.user
        cart = Cart.objects.filter(user=user)
        context = {
            'cart': cart
        }
        return render(request, 'cart/cart.html', context) 
    # cart = Cart.objects.get(user=user)
    # context = {
    #     'cart': cart
    # }

    # if request.user.is_authenticated:
    #     user=request.user
    #     Cart.objects.filter(user=user).delete()
    #     product_id = request.POST['product']
        # product = Product.objects.get(pk=product_id)
    #     # cart, _ = Cart.objects.get_or_create(user=user, product=product)    
    #     cart.amount=int(request.POST['count'])
    #     # cart.total_price = cart.amount * product.price
    #     if cart.amount>0:
    #         cart.total_price = cart.amount * product.price
    #         cart.save()
    #     # order 뷰로 리디렉션
    #     return redirect('/order/')
    # else : 
    #     return redirect('/accounts/login/')    
    
    # 결제하기 버튼 눌렀을 때     
    # 수량 및 옵션 변경  
    if request.method == 'POST':
        return redirect('orders:orders')
        

# 카트목록 삭제 버튼 클릭 시 
def cart_delete(request, pk):
    object = Cart.objects.get(pk=pk)
    object.delete()  
    return redirect('cart:cart')

   