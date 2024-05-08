from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .models import Order
from seller_product.models import Product,Cart
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

@login_required
def order(request):    
     # 현재 로그인한 사용자의 카트 정보를 가져오기
    user = request.user
    cart_items = Cart.objects.filter(user=user)   
    products = []
    for one in cart_items: 
        product_id = one.product_id
        product = get_object_or_404(Product, product_id=product_id)
        products.append(product)
             
    context = {
        'object': cart_items, 
        'product': products,
    }

    if request.method == 'GET':
        return render(request, template_name='order/order.html', context=context)

    elif request.method == 'POST':
        # cart_items는 list 여러개일 경우 나중에 리스트형태에서 뽑아와야함
        # order = Order.objects.create(
        #     user=user,
        #     product=product,
        #     amount = cart_items[0].amount,
        #     total_price=cart_items[0].total_price,
        #     payment_total_price=cart_items[0].payment_total_price,
        #     order_date=timezone.now(),
        #     payment_date=timezone.now(),
        #     pay_confirm = True)
    
        # order.save()
        # 주문 생성 후 카트 비우기
        cart_items.delete()            
        
         # 주문 완료 페이지로 리다이렉션
        return redirect('order:order_done')  
        # return render(request, template_name='order/order_done.html', context=context)

# 템플릿에서 받아야함
@login_required
def password_confirm(request):
     # POST 요청이 아닌 경우에는 에러를 반환
    if request.method != 'POST':
        return JsonResponse({'message': '잘못된 요청입니다.'}, status=400)
    
    # 사용자가 입력한 비밀번호 가져오기
    input_password = request.POST.get('input_password')

    # 현재 로그인한 사용자의 id가져오기
    user = request.user
    
    # 입력한 비밀번호와 저장된 비밀번호를 비교하여 일치 여부 확인
    user = authenticate(username=user, password=input_password)

    user = request.user
    cart_items = Cart.objects.filter(user=user)   
    
    # cart_items는 list 여러개일 경우 나중에 리스트형태에서 뽑아와야함
    order = Order.objects.create(
            user=user,
            product=cart_items[0].product,
            amount = cart_items[0].amount,
            total_price=cart_items[0].total_price,
            payment_total_price=cart_items[0].payment_total_price,
            order_date=timezone.now(),
            payment_date=timezone.now(),
            pay_confirm = True)
    
    order.save()

    if user is not None:
        return JsonResponse({'message': '비밀번호가 확인되었습니다.'})
    else:
        return JsonResponse({'message': '비밀번호가 맞지 않습니다.'}, status=401)
    
    

@login_required
def order_done(request):
    user = request.user
    last_order = Order.objects.filter(user=user).order_by('-pk')[0]   
    
    context = {
    'object': last_order    
    }   
    # 결제 완료 페이지로 리디렉션
    return render(request, 'order/order_done.html', context)
   
def order_list(request):
    user = request.user
    order = Order.objects.filter(user=user)  
    
    page = request.GET.get('page',1)    

    paginator = Paginator(order, 7)
    page_obj = paginator.page(page)
    context = {
        'page_obj':page_obj
    }
    return render(request, 'order/order_list.html', context)
def order_detail(request, pk):
    user = request.user
    last_order = Order.objects.get(user=user, pk=pk)
    context = {
        'object': last_order
    }
    return render(request, 'order/order_detail.html', context)