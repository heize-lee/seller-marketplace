from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden,JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from .models import Review,Product
from orders.models import Order
from .forms import ReviewCreateForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
# Create your views here.

# class ReviewCreate(CreateView):
#     model = Review
#     fields = ['rating','comment','image']

from django.shortcuts import render

def review_list(request, section):
    # 로직 구현
    return render(request, 'reviews/review_list.html', {'section': section})

def ReviewCreate(request):
    
    if request.method =='GET':
        product_id = request.GET['product']
        product = Product.objects.get(pk=product_id)
        form = ReviewCreateForm()
        if not request.user.is_authenticated:
            return redirect('/accounts/login/') # 로그인 페이지로 리디렉션
        if request.user.is_authenticated and request:
            if Review.objects.filter(user=request.user, product=product).exists():
                messages.error(request, "이미 작성된 리뷰가 있습니다.")
                return redirect('/product/'+ product_id,)  # 제품 상세 페이지로 리디렉션
            if not Order.objects.filter(user=request.user, product=product):
                messages.error(request, "구매한 상품만 후기작성 가능합니다.")
                return redirect('/product/'+product_id)
    if request.method == 'POST':
        form = ReviewCreateForm(request.POST,request.FILES)
         
        product_id = request.POST['product']
        product = Product.objects.get(pk=product_id)
        if request.POST['rating']=='0':
            form.add_error('rating', ' 평점을 선택해주세요.')
            if request.POST['comment']=='':
                form.add_error('comment', ' 후기를 작성해주세요.')
            return render(request, 'reviews/review_form.html', {'form': form, 'product': product})
        if request.POST['comment']=='':
            form.add_error('comment', ' 후기를 작성해주세요.')
            return render(request, 'reviews/review_form.html', {'form': form, 'product': product})
        
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # 현재 로그인된 사용자
            review.product = product
            review.rating = float(request.POST['rating'])
            # if 'image' in request.FILES:
            #     review.image = request.FILES['image']
            review.save()
            return redirect('/product/'+product_id)
        
       
    return render(
        request,
        'reviews/review_form.html',
        {'form':form,
         'product':product,
        }
    )
#리뷰삭제
@require_http_methods(["DELETE"])
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if request.user == review.user:  # 리뷰 작성자만 삭제할 수 있도록 합니다.
        review.delete()
        return JsonResponse({'success': '리뷰가 삭제되었습니다.'})
    else:
        return JsonResponse({'error': '리뷰를 삭제할 권한이 없습니다.'}, status=403)
    

#리뷰수정
def put_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    
    if request.method == 'POST':
        form = ReviewCreateForm(request.POST,request.FILES,instance=review)
        product_id = request.POST['product']
        product = Product.objects.get(pk=product_id)
        
        if request.POST['rating']=='0':
            form.add_error('rating', ' 평점을 선택해주세요.')
            if request.POST['comment']=='':
                form.add_error('comment', ' 후기를 작성해주세요.')
            return render(request, 'reviews/review_update.html', {'form': form, 'product': product ,'review':review})
        if request.POST['comment']=='':
            form.add_error('comment', ' 후기를 작성해주세요.')
            return render(request, 'reviews/review_update.html', {'form': form, 'product': product,'review':review})
        # try:
        #     reviews = Review.objects.filter(product_id=product.product_id)
        #     cnt = reviews.count()
        #     if cnt > 0 :
        #         reviews_rating_mean = sum([i.rating for i in reviews])/cnt
        #          # 평균 rating 값을 product 모델의 average_rating 필드에 저장
        #     else:
        #         reviews_rating_mean = 0
        #     product.average_rating = reviews_rating_mean
        #     product.save()
        # except:
        #     pass  
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # 현재 로그인된 사용자
            
            review.rating = float(request.POST['rating'])
            # if 'image' in request.FILES:
            #     review.image = request.FILES['image']
            review.save()
            return redirect('/product/'+product_id)
    else:
        product_id = request.GET['product']
        product = Product.objects.get(pk=product_id)
        form = ReviewCreateForm(instance=review)
    return render(
        request,
        'reviews/review_update.html',
        {'form':form,
         'product':product,
         'review':review,
         'MEDIA_URL' : settings.MEDIA_URL
        }
    )

def review_list(request,section):
    review = Review.objects.filter(user=request.user)
    return render(
        request,
        'reviews/my_review_list.html',
        {
            'review':review
        }
    )
# from django.shortcuts import get_object_or_404
# def ReviewCreate(request,order_id):
#     obj = get_object_or_404(Order, id=order_id, user=request.user)

#     if request.method == 'POST':
#         form = ReviewCreateForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse('처리완료')
#     else:
#         form = ReviewCreateForm()

#     return render(
#         request,
#         'reviews/review_form.html',
#         {'form':form,
#          'product':product
#         }
#     )
  
# 리뷰작성 유효성 검사 '/reviews/create/<int:order_id>' or '/product_detail/product_id/' 리다이렉트
# views.detail
# def review_create_from(request):
#     if request.user.is_authenticated:
#         user=request.user
#         product_id = request.POST['product']
        # order_id = Order.objects.fillter(user=request.user,product_id=product_id)
        # product = Product.objects.get(pk=product_id)
        # if not order_id:
        #      return redirect('/product_detail/product_id/') 
        # if Review.objects.filter(order_id=order_id).exists():
        #      return redirect('/product_detail/product_id/') 
        # return redirect('/reviews/create/<int:order_id>')
        # return redirect('/create/')
  