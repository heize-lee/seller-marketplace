from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from .models import Product, Category
from .forms import RegisterForm 
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages

#리뷰모델(회성)
from reviews.models import Review
from django.db.models import Avg
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import F


class ProductCreate(LoginRequiredMixin, FormView):

    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'
    login_url = reverse_lazy('account_login')  # 로그인 페이지의 URL

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
    



from django.db.models import Min, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import ProductFilter

from django.views.generic import ListView
from django.db.models import Min, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'
    paginate_by = 15

    def get_queryset(self):
        queryset = Product.objects.only(
            'product_id', 'product_name', 'product_price', 'stock_quantity', 'created_date', 'updated_date', 'category_id', 'product_img', 'seller_email'
        ).all()

        # 카테고리 필터링 추가
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

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

        # 모든 카테고리 가져오기
        categories = Category.objects.all()
        context['categories'] = categories

        # 현재 선택된 카테고리 이름 추가
        category_id = self.request.GET.get('category')
        if category_id:
            context['category_name'] = Category.objects.get(id=category_id).category_name
        else:
            context['category_name'] = '전체'

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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDetail(DetailView):
    model = Product   
    template_name = 'product_detail.html'
    context_object_name = 'product'
    
    #추천상품 선정+리뷰 데이터 할당(회성)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        recommended_products = Product.objects.filter(category=product.category).exclude(pk=product.pk).order_by('?')[:3]
        reviews = Review.objects.filter(product_id=product.product_id).order_by('-created_at')
        cnt = reviews.count()
        if cnt > 0 :
            reviews_rating_mean = sum([i.rating for i in reviews])/cnt
            product.average_rating = reviews_rating_mean
            product.save()
        else:
            reviews_rating_mean = 0
        
        # 별점 백분율 계산
        if cnt == 0:
            rating = {
            '1' : 0,
            '2' : 0,
            '3' : 0,
            '4' : 0,
            '5' : 0
        }
        else:
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
        context['recommended_products'] = recommended_products
        context['reviews'] = page_obj
        context['average_rating'] = average_rating
        context['count'] = cnt
        context['rating'] = rating
        context['paginator']=paginator
        context['page_number']=page_number
        context['review_rating_mean']=reviews_rating_mean
        return context
        
    
    
#리뷰 비동기 요청(회성)
def review(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        
        reviews = Review.objects.filter(product=product).annotate(nickname=F('user__nickname'), email=F('user__email')).values('id','email','nickname','comment', 'rating', 'created_at','image').order_by('-created_at')
        if request.GET.get('select') == 'rating_height':
            reviews = reviews.order_by('created_at')
         # Paginator 설정
        paginator = Paginator(reviews, 5)  # 페이지당 5개의 리뷰
        page_number = int(request.GET.get('page',1))  # GET 파라미터에서 페이지 번호를 가져옴
        page_obj = paginator.get_page(page_number)
        # reviews_list = list(reviews)
        reviews_list =list(page_obj.object_list)
    
        return JsonResponse(reviews_list, safe=False)
    else:
        # 다른 HTTP 메소드 또는 ajax 요청이 아닌 경우 처리
        return JsonResponse({'error': 'Invalid request'}, status=400)
#카트 구매 코드 주석 처리 해놓음

    
#기존 카트 구매 코드 주석 처리 해놓음
    # def post(self, request, *args, **kwargs):
    #     # 상품 디테일 페이지에서 바로구매를 누르면 해당 상품이 카트 테이블에 추가
    #     product = self.get_object()
    #     user = request.user
    #     cart_item = Cart.objects.get_or_create(user=user, product=product)
    #     cart_item.save()
        
    #     # 주문 페이지로 리디렉션합니다.
    #     return redirect('order')

#각 판매자 판매물품 
class ProductListByUser(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'my_products.html'
    context_object_name = 'my_products'
    login_url = reverse_lazy('account_login')  # 로그인 페이지의 URL

    def get_queryset(self):
        # 로그인한 사용자의 이메일을 기준으로 해당 사용자가 작성한 판매글만 필터링하여 반환
        user_email = self.request.user.email
        queryset = Product.objects.filter(seller_email=user_email).values('pk', 'product_id', 'product_name', 'product_img', 'product_price')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context

    def dispatch(self, request, *args, **kwargs):
        # 로그인된 사용자만 접근 가능하도록 처리
        if not self.request.user.is_authenticated:
            # 로그인되어 있지 않은 경우 로그인 페이지로 리디렉션
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

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

