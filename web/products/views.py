from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from .models import Product, Category
from .forms import RegisterForm 
from django.urls import reverse_lazy
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings



class ProductCreate(FormView):                           #class ProductCreate(LoginRequiredMixin, FormView):
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
        #if not self.request.user.is_authenticated:
            # 로그인되어 있지 않은 경우 로그인 페이지로 리디렉션
            #return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    



from django.db.models import Min, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import ProductFilter

from django.views.generic import ListView
from django.db.models import Min, Max
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'
    paginate_by = 3

    def get_queryset(self):
        queryset = Product.objects.only('product_id', 'product_name', 'product_price', 'stock_quantity', 'created_date', 'updated_date', 'category_id', 'product_img', 'seller_email').all()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)

        sort_option = self.request.GET.get('sort', 'created_date')
        order = self.request.GET.get('order', 'desc')

        if order == 'asc':
            sort_option = sort_option
        else:
            sort_option = '-' + sort_option

        queryset = self.filterset.qs.order_by(sort_option)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        context['sort'] = self.request.GET.get('sort', 'created_date')
        context['order'] = self.request.GET.get('order', 'desc')
        context['filterset'] = self.filterset

        # 모든 상품의 최소 가격과 최대 가격을 쿼리
        min_price = Product.objects.aggregate(Min('product_price'))['product_price__min']
        max_price = Product.objects.aggregate(Max('product_price'))['product_price__max']

        context['min_price'] = min_price
        context['max_price'] = max_price

        # 필터된 결과에 대한 페이지네이션 설정
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['page_obj'] = page_obj
        return context



class ProductDetail(DetailView):
    model=Product   
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    
#카트 구매 코드 주석 처리 해놓음
    # def post(self, request, *args, **kwargs):
    #     # 상품 디테일 페이지에서 바로구매를 누르면 해당 상품이 카트 테이블에 추가
    #     product = self.get_object()
    #     user = request.user
    #     cart_item = Cart.objects.get_or_create(user=user, product=product)
    #     cart_item.save()
        
    #     # 주문 페이지로 리디렉션합니다.
    #     return redirect('order')


#각 판매자 판매물품 
class ProductListByUser(ListView):
    model = Product
    template_name = 'my_products.html'
    context_object_name = 'my_products'

    def get_queryset(self):
        # 로그인한 사용자의 이메일을 기준으로 해당 사용자가 작성한 판매글만 필터링하여 반환
        user_email = self.request.user.email
        queryset = Product.objects.filter(seller_email=user_email).values('pk', 'product_id', 'product_name', 'product_img', 'product_price')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context

#기존view 
#class ProductListByUser(ListView):
    #model = Product
    #template_name = 'my_products.html'
    #context_object_name = 'my_products'

    #def get_queryset(self):
        #user_email = self.request.user.email
        #return Product.objects.filter(seller_email=user_email)
    

#업데이트 view
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['product_name', 'product_price', 'description', 'stock_quantity', 'category', 'product_img']
    template_name = 'product_update.html'
    success_url = reverse_lazy('product:my_products')

#삭제 view
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product:my_products')  # 삭제 후 이동할 URL

    # 템플릿 파일 이름 지정
    template_name = 'product_confirm_delete.html'
