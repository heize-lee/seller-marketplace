from django.shortcuts import render, redirect
from cart.models import Cart,Product
from django.views.decorators.csrf import csrf_exempt
import os
import dotenv


# Create your views here.
dotenv.load_dotenv()
@csrf_exempt
def orders(request):
    if request.method == 'GET':
        user = request.user
        # 바로구매
        if 'detail' in request.GET:
            product_id = request.GET.get('product_id')
            product = Product.objects.get(product_id=product_id)
            quantity = request.GET.get('cnt')
            total_price = request.GET.get('total_price')
            context = {
            'user': user,
            'product':product,
            'quantity':quantity,
            'total_price':total_price,
            }
            return render(request, 'orders/orders.html',context)
        # 카트에서 구매
        cart = Cart.objects.filter(user=user)
        print(request.method)
        # js코드 복잡해짐
        # 등록된 배송지가 없음 > 지워지고 
        # AJAX로 
        # 새로고침은 배송정보부분만 고침
        # 배송지 정보 불러옴
        # Address.objects.get()
        context = {
            'cart': cart,
            'user': user,
        }
        return render(request,'orders/orders.html', context)
    # if request.method == 'POST':
        
        
        # 모달 정보 address테이블에 저장
# 배송지 view
# 결제정보 view
# 결제하기 view

def orders_cart_delete(request,pk):
    object = Cart.objects.get(pk=pk)
    object.delete()  
    return redirect('orders:orders')

def order_done(request):
    return render(request, 'orders/order_done.html')