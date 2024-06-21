from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from products.models import Product
from django.http import JsonResponse
# Create your views here.
def cart(request):
    # 카트페이지 처음 들어왔을 때 
    if request.method == 'GET':
        user = request.user
        cart = Cart.objects.filter(user=user)
        payment_total_price = sum(i.total_price for i in cart)
        context = {
            'cart': cart,
            'payment_total_price':payment_total_price
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

# 장바구니버튼 클릭시 담기
def add_cart(request,product_id):
    product = get_object_or_404(Product,product_id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    cart_item.amount += 1
    cart_item.total_price = cart_item.amount * product.product_price
    cart_item.save()
    
    return redirect('cart:cart')
# 카트에서 수량추가
def plus_cart(request):
    product_id=request.GET.get('product_id')
    product = Product.objects.get(product_id=product_id)
    cart_item = Cart.objects.get(user=request.user, product_id=product_id)
    if cart_item.amount>0:
        cart_item.amount += 1
    cart_item.total_price = cart_item.amount * product.product_price
    cart_item.save()

    # 모든 카트 항목의 총합 계산
    cart_items = Cart.objects.filter(user=request.user)
    total_payment = sum(item.total_price for item in cart_items)
    return JsonResponse({
                'amount': cart_item.amount,
                'total_price': cart_item.total_price,
                'payment_total_price': total_payment
            })
#카트에서 수량빼기
def minus_cart(request):
    product_id=request.GET.get('product_id')
    product = Product.objects.get(product_id=product_id)
    cart_item = Cart.objects.get(user=request.user, product_id=product_id)
    if cart_item.amount>1:
        cart_item.amount -= 1
    cart_item.total_price = cart_item.amount * product.product_price
    cart_item.save()

    # 모든 카트 항목의 총합 계산
    cart_items = Cart.objects.filter(user=request.user)
    total_payment = sum(item.total_price for item in cart_items)
    return JsonResponse({
                'amount': cart_item.amount,
                'total_price': cart_item.total_price,
                'payment_total_price': total_payment
            })
