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
    


class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'




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
