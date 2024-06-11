from django.shortcuts import render
from cart.models import Cart

# Create your views here.
def orders(request):
    if request.method == 'GET':
        user = request.user
        cart = Cart.objects.all()
        context = {
            'cart': cart,
            'user': user
        }
        return render(request,'orders/orders.html', context)
    if request.method == 'POST':
        pass
    