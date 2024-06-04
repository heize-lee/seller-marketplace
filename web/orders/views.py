from django.shortcuts import render

# Create your views here.
def orders(request):
    if request.method == 'GET':
        return render(request,'orders/orders.html')
    if request.method == 'POST':
        pass
    