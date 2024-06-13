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
#리뷰모델(회성)
from reviews.models import Review
from django.db.models import Avg
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
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
    #리뷰 데이터 할당(회성)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        reviews = Review.objects.filter(product_id=product.product_id).order_by('-created_at')
        cnt = reviews.count()
        # 별점 백분율 계산
        rating = {
            '1' : reviews.filter(Q(rating=1) | Q(rating=0.5)).count()/cnt * 100,
            '2' : reviews.filter(Q(rating=2) | Q(rating=1.5)).count()/cnt * 100,
            '3' : reviews.filter(Q(rating=3) | Q(rating=2.5)).count()/cnt * 100,
            '4' : reviews.filter(Q(rating=4) | Q(rating=3.5)).count()/cnt * 100,
            '5' : reviews.filter(Q(rating=5) | Q(rating=4.5)).count()/cnt * 100
        }

        # Paginator 설정
        paginator = Paginator(reviews, 5)  # 페이지당 5개의 리뷰
        page_number = int(self.request.GET.get('page',1))  # GET 파라미터에서 페이지 번호를 가져옴
        page_obj = paginator.get_page(page_number)
    
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        context['reviews'] = page_obj
        context['average_rating'] = average_rating
        context['count'] = cnt
        context['rating'] = rating
        context['paginator']=paginator
        context['page_number']=page_number
        return context
    def get(self, request, *args, **kwargs):
        if request.GET.get('ajax'):
            product = self.get_object()
            reviews = Review.objects.filter(product_id=product.product_id).order_by('-created_at')
            review_list = reviews.values('user', 'created_at', 'comment', 'rating', 'code')
            return JsonResponse(list(review_list), safe=False)
        
        return super().get(request, *args, **kwargs)
#카트 구매 코드 주석 처리 해놓음
    # def post(self, request, *args, **kwargs):
    #     # 상품 디테일 페이지에서 바로구매를 누르면 해당 상품이 카트 테이블에 추가
    #     product = self.get_object()
    #     user = request.user
    #     cart_item = Cart.objects.get_or_create(user=user, product=product)
    #     cart_item.save()
        
    #     # 주문 페이지로 리디렉션합니다.
    #     return redirect('order')


#리뷰 리스트(회성)
# def review_list(request):
#     # 리뷰 리스트를 반환하는 로직

#     return render(request, 'reviews/review_list.html')