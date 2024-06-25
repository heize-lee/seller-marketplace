# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart,Product
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from accounts.models import DeliveryAddress
from payment.models import Payment
from orders.models import Order
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
@login_required
@csrf_exempt
def orders(request):
    if request.method == 'GET':
        user = request.user

        cart = Cart.objects.filter(user=user)
        delivery_address = DeliveryAddress.objects.filter(user=user)

        # if 바로구매 boolean True
        # 단일건에 해당되는 카트 튜플만 가져오고
        # else cart에 담긴 여러개의 상품을 가져온다

            # 기본 배송지 정보를 가져옵니다. (존재하지 않으면 except 블록으로 이동)
            # default_delivery_address = DeliveryAddress.objects.filter(user=user, is_default=True)[0]
            
        default_delivery_address = DeliveryAddress.objects.filter(user=user, is_default=True).first()


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
                'default_delivery_address': default_delivery_address,
                'delivery_address': delivery_address,
                'is_direct': True,
                
            }
            return render(request, 'orders/orders.html',context)
        
        # 카트에서 구매
        payment_total_price = sum(i.total_price for i in cart)
        print(request.method)

        context = {
            'cart': cart,
            'user': user,
            'default_delivery_address': default_delivery_address,
            'delivery_address': delivery_address,
            'payment_total_price': payment_total_price,
            'is_direct': False,


        }
        return render(request,'orders/orders.html', context)
    
    elif request.method == 'POST' :
        # 주문정보 삭제 시 
        if 'orders_cart_delete' in request.POST:
            return redirect('orders:orders_cart_delete')
        
        user = request.user
        # form에서 받은 input값
        recipient = request.POST.get('recipient')
        phone = request.POST.get('phone')
        destination = request.POST.get('destination')
        postal_code = request.POST.get('postal_code')
        address = request.POST.get('address')
        detailed_address = request.POST.get('detailed_address')
        
        is_default = request.POST.get('default_delivery_hidden') == 'on'  # 기본 배송지 체크박스의 값 확인
        # 처음 배송지 추가시 disabled된 input-hidden으로 기본배송지 추가
        
            # !!!!!!!!!배송지 수정에서 추가하기를 했을 때
        

        default_delivery_checkbox = request.POST.get('default_delivery') == 'on' or is_default
        if default_delivery_checkbox:
            is_default = True
        else:
            is_default = False
        
        if is_default:
            DeliveryAddress.objects.filter(user=user, is_default=True).update(is_default=False)

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

@csrf_exempt
def set_default_delivery(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        delivery_id = data.get('delivery_id')
        
        # 모든 기존 기본 배송지를 False로 설정
        DeliveryAddress.objects.filter(is_default=True).update(is_default=False)
        
        # 선택한 배송지를 기본 배송지로 설정
        delivery = get_object_or_404(DeliveryAddress, id=delivery_id)
        delivery.is_default = True
        delivery.save()
        # DeliveryAddress.objects.filter(id=delivery_id).update(is_default=True)
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
        # 모달 정보 address테이블에 저장
# 배송지 view
# 결제정보 view
# 결제하기 view

def orders_cart_delete(request,pk):
    # cart 삭제 
    user = request.user
    object = Cart.objects.filter(user=user, product_id=pk)
    object.delete()  
    return redirect('orders:orders')
    # 바로구매 product삭제

@login_required
def order_done(request):
    user = request.user
    order = Order.objects.filter(user=user).last()
    payment = Payment.objects.get(order=order)
    context = {
        'payment': payment,
        'order': order,

    }
    return render(request, 'orders/order_done.html', context)