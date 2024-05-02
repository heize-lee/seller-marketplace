from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Product,Category, Cart
from .forms import RegisterForm

# from order.forms import RegisterForm as OrderForm



class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'

class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
 
class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = OrderForm(self.request)
    #     return context

# class ProductList(ListView):
#     model = Product
#     ordering = '-pk'

# def category_page(request,slug):  
#     category = Category.objects.get(slug=slug)
#     product_list = Product.objects.filter(category=category)

#     return render(
#         request,
#         'product/product_list.html',
#         {
#             'product_list': product_list,
#             'categories': Category.objects.all(),
#             'category':category
#         }
#     )

# class ProductDetail(DetailView):
#     model=Product
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#          # 현재 페이지의 Product 객체를 가져옵니다.
#         product = self.get_object()
        
#         # 현재 Product 객체와 관련된 Cart 객체를 필터링합니다.
#         context['carts'] = Cart.objects.filter(product_id=product.product_id)
#         return context

from django.http import JsonResponse

def modify_cart(request):
    
    product_id = request.POST['productId']
    product = Product.objects.get(pk=product_id)
    cart, _ = Cart.objects.get_or_create(product=product)    
    cart.amount=int(request.POST['amountChange'])
    if cart.amount>0:
        cart.save()
        
    # 변경된 최종 결과를 반환(JSON)
    context = {
        'newQuantity':cart.amount, 
        'message':'수량이 성공적으로 업데이트 되었습니다.',
        'success':True
    }
    return JsonResponse(context)

