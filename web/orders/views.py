from django.shortcuts import render, redirect
from cart.models import Cart
from django.views.decorators.csrf import csrf_exempt
import os
import dotenv
import urllib.parse
import requests

# 지현
from .models import Order 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order

# 지현 (order_list)
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)  # 현재 로그인한 사용자의 주문만 필터링
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def mypage_section(request, section):
    context = {}
    if section == 'orders':
        return order_list(request)  # order_list 뷰를 호출하여 같은 템플릿을 사용
    elif section == 'edit_profile':
        # 다른 섹션 처리
        template_name = 'accounts/edit_profile.html'
    else:
        # 기본 섹션 처리
        template_name = f'accounts/{section}.html'
    
    return render(request, template_name, context)


# Create your views here.
dotenv.load_dotenv()
@csrf_exempt
def orders(request):
    if request.method == 'GET':
        user = request.user
        cart = Cart.objects.all()
        print(request.method)
        storeId=os.getenv("storeId")
        channelKey=os.getenv("channelKey")
        # js코드 복잡해짐
        # 등록된 배송지가 없음 > 지워지고 
        # AJAX로 
        # 새로고침은 배송정보부분만 고침
        # 배송지 정보 불러옴
        # Address.objects.get()
        context = {
            'cart': cart,
            'user': user,
            "storeId":storeId,
            "channelKey":channelKey
        }
        return render(request,'orders/orders.html', context)
    elif request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if payment_method == 'kakao_pay':
            return redirect('payment:kakao_payment')
        return redirect('orders:order_done')

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