from django.shortcuts import render
from .models import Cart
# from products.models import Product
# Create your views here.
def cart(request):
    # if request.user.is_authenticated:
    #     user=request.user
    #     Cart.objects.filter(user=user).delete()
    #     product_id = request.POST['product']
    #     # product = Product.objects.get(pk=product_id)
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
    return render(request, 'cart/cart.html')