from django.shortcuts import render, redirect
from cart.models import Cart,Product
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from accounts.models import DeliveryAddress
import os
import dotenv
import urllib.parse
import requests


# Create your views here.
dotenv.load_dotenv()
@csrf_exempt
def orders(request):
    if request.method == 'GET':
        user = request.user

        cart = Cart.objects.filter(user=user)
        delivery_address = DeliveryAddress.objects.all()

        # if 바로구매 boolean True
        # 단일건에 해당되는 카트 튜플만 가져오고
        # else cart에 담긴 여러개의 상품을 가져온다

        try:
            # 기본 배송지 정보를 가져옵니다. (존재하지 않으면 except 블록으로 이동)
            default_delivery_address = DeliveryAddress.objects.filter(user=user, is_default=True)[0]
        except DeliveryAddress.DoesNotExist:
            default_delivery_address = None


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
            'default_delivery_address': default_delivery_address,
            'delivery_address': delivery_address,
        }
        return render(request,'orders/orders.html', context)
    
    elif request.method == 'POST' :
        user = request.user
        # form에서 받은 input값
        recipient = request.POST.get('recipient')
        phone = request.POST.get('phone')
        destination = request.POST.get('destination')
        postal_code = request.POST.get('postal_code')
        address = request.POST.get('address')
        detailed_address = request.POST.get('detailed_address')
        # 처음 배송지 추가시 disabled된 input-hidden으로 기본배송지 추가
        is_default = True if request.POST.get('default_delivery_hidden') == 'on' else False
        # 수정모달에서 배송지 추가시 기본 배송지 체크여부에 따라 기본배송지 변경 
        # 이전에 is_default가 True인 기본배송지는 False로 변경
        # is_default = True if request.POST.get('default_delivery') == 'on' else False


        # 기본 배송지가 있는지 확인
        # if is_default:
        # # 기본 배송지가 있는지 확인하고, 있으면 기존 기본 배송지를 False로 설정
        #     try:
        #         old_default_address = DeliveryAddress.objects.get(user=user, is_default=True)
        #         old_default_address.is_default = False
        #         old_default_address.save()
        #     except DeliveryAddress.DoesNotExist:
        #         pass  # 기본 배송지가 없으면 pass

        delivery_address = DeliveryAddress.objects.create(
            user = user,
            recipient = recipient,
            phone_number = phone,
            destination = destination,
            postal_code = postal_code,
            address = address,
            detail_address = detailed_address,
            is_default = is_default
        )        
        
        delivery_address.save()


       
        return redirect('orders:orders')


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