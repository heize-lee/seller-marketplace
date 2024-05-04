from django.shortcuts import render,redirect

from .models import Order
from seller_product.models import Product,Cart
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.
def order(request):    
     # 현재 로그인한 사용자의 카트 정보를 가져오기
    user = request.user
    
    cart_items = Cart.objects.filter(user=user.id)   
    # cart_items = Cart.objects.all()
    products = []
    for one in cart_items: 
        product_id = one.product_id
        print(product_id)
        product = get_object_or_404(Product, product_id=product_id)
        products.append(product)


    # product_id = cart_items[0].product_id
    # product_id = request.POST.get('product_id')  # 요청에서 실제로 사용자가 주문하려는 상품의 ID를 가져오기
    # product = get_object_or_404(Product, product_id=product_id)  # ID에 해당하는 Product 객체 가져오기
    
        
    context = {

    'object': cart_items, 
    'product': products,
    }
    return render(request, template_name='order/order_detail.html', context=context)

def order_done(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)   
    product_id = cart_items.product_id
    product = get_object_or_404(Product, product_id=product_id)  # ID에 해당하는 Product 객체 가져오기

    # 결제하기를 눌렀을 때 주문 테이블에 카트 테이블의 내용을 저장
    if request.method == 'POST':

        # 카트에 담긴 각 상품에 대한 주문을 생성
        try:
            order = Order.objects.get(user=user, product=product) 
        except Order.DoesNotExist:
            # 주문이 존재하지 않으면 새로운 주문을 생성
            order = Order.objects.create(user=user, product=product, order_date=timezone.now(), payment_date=timezone.now(), pay_confirm = True)

        # for cart_item in cart_items:
        #     order = Order.objects.create(
        #         user=user,
        #         product=cart_item.product,
        #         order_date=timezone.now()
        #     )
        
        order.save()

         # 결제가 완료되면 카트 테이블의 내용을 삭제
        cart_items.delete()
        # 결제 완료 페이지로 리디렉션
        return render(request, 'order/order_done.html')
    order = Order.objects.all()
    context = {
        'object': order
    }
    return render(request,'order/order_done.html', context)