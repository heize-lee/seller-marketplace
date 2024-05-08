<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView, CreateView
from .models import Product, Category, Cart
from .forms import RegisterForm
from django.views.generic import DetailView
from .models import Product
=======
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from .models import Product,Category, Cart
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# from order.forms import RegisterForm as OrderForm
>>>>>>> 113d0feeba7d97506ab015661227177974901d6b


@login_required
def modify_cart(request):
    if request.method == 'POST':
        user = request.user
        Cart.objects.filter(user=user).delete()
        product_id = request.POST['product']
        product = Product.objects.get(pk=product_id)
        cart, _ = Cart.objects.get_or_create(user=user, product=product)    
        cart.amount = int(request.POST['count'])
        if cart.amount > 0:
            cart.total_price = cart.amount * product.price
            cart.save()
        return redirect('/order/')
    else:
        return redirect('home')

class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'

class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'  # 이 부분은 적절한 템플릿 파일명으로 수정하세요.
    context_object_name = 'product'

def category_page(request, slug):  
    category = Category.objects.get(slug=slug)
    product_list = Product.objects.filter(category=category)

    return render(
        request,
        'product.html',
        {
            'product_list': product_list,
            'categories': Category.objects.all(),
            'category': category
        }
    )

<<<<<<< HEAD
class ProductCreate(CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'category']
    template_name = 'product_create.html'
    success_url = '/product/'  # 적절한 URL로 수정하세요.
=======
class ProductCreate(LoginRequiredMixin, FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'
    login_url = reverse_lazy('accounts:login')  # 로그인 페이지의 URL

    def form_valid(self, form):
        # 로그인된 사용자의 이메일 가져오기
        email = self.request.user.email

        # 폼에서 인스턴스 생성
        product_instance = form.save(commit=False)
        product_instance.seller_email = email  # 판매자 이메일 저장
        product_instance.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # 사용자가 로그인되어 있는지 확인
        if not self.request.user.is_authenticated:
            # 로그인되어 있지 않은 경우 로그인 페이지로 리디렉션
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
        
        
 
class ProductDetail(DetailView):
    model=Product   
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        # 상품 디테일 페이지에서 바로구매를 누르면 해당 상품이 카트 테이블에 추가
        product = self.get_object()
        user = request.user
        cart_item = Cart.objects.get_or_create(user=user, product=product)
        cart_item.save()
        
        # 주문 페이지로 리디렉션합니다.
        return redirect('order')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = OrderForm(self.request)
    #     return context

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#          # 현재 페이지의 Product 객체를 가져옵니다.
#         product = self.get_object()
        
#         # 현재 Product 객체와 관련된 Cart 객체를 필터링합니다.
#         context['carts'] = Cart.objects.filter(product_id=product.product_id)
#         return context

from django.http import JsonResponse


def modify_cart(request):
    if request.user.is_authenticated:
        user=request.user
        Cart.objects.filter(user=user).delete()
        product_id = request.POST['product']
        product = Product.objects.get(pk=product_id)
        cart, _ = Cart.objects.get_or_create(user=user, product=product)    
        cart.amount=int(request.POST['count'])
        if cart.amount>0:
            cart.save()
        # order 뷰로 리디렉션
        return redirect('/order/')
    else : 
        return redirect('/accounts/login/')    


    # 변경된 최종 결과를 반환(JSON)
    # context = {
    #     'newQuantity':cart.amount, 
    #     'message':'수량이 성공적으로 업데이트 되었습니다.',
    #     'success':True
    # }
    # return JsonResponse(context)

from django.db.models import Q
class ProductSearch(ProductList):
    def get_queryset(self) :
        q = self.kwargs['q']
        product_list = Product.objects.filter(
            Q(product_name__contains=q) | Q(description__contains=q)
        ).distinct()
        return product_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f"Search: {q}"

        return context
    





#작성글 리스트 

class ProductListByUser(ListView):
    model = Product
    template_name = 'my_products.html'
    context_object_name = 'my_products'

    def get_queryset(self):
        # 로그인한 사용자의 이메일을 기준으로 해당 사용자가 작성한 판매글만 필터링하여 반환
        user_email = self.request.user.email
        return Product.objects.filter(seller_email=user_email)
    

#update view
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['product_name', 'price', 'description', 'quantity', 'total_price', 'category', 'image']
    template_name = 'product_update.html'
    success_url = reverse_lazy('product:my_products')

#삭제 view
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product:my_products')  # 삭제 후 이동할 URL

    # 템플릿 파일 이름 지정
    template_name = 'product_confirm_delete.html'

>>>>>>> 113d0feeba7d97506ab015661227177974901d6b
