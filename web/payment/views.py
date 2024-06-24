from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import uuid
import requests
import json
import os
import dotenv
import urllib.parse
from cart.models import Cart
from products.models import Product
from orders.models import Order, OrderItems
from .models import Payment
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction


from .services import SampleService

# Create your views here.

# 고유한 주문 번호 생성
order_no = str(uuid.uuid4())


""" .env file
storeId=
channelKey=
billing_key=
PORTONE_API_KEY= #portone v2 api key
"""
dotenv.load_dotenv()
# 카드결제 시 포트원
@csrf_exempt
def portone_payment(request):
    if request.method == "POST":
        pass
     

            # url: "https://api.portone.io/billing-keys"
            # method: "post"
            # headers: { Authorization: `PortOne ${PORTONE_API_SECRET}` },
            # data: {
            #         storeId: "store-4ff4af41-85e3-4559-8eb8-0d08a2c6ceec", // 고객사 storeId로 변경해주세요.
            #         channelKey: "channel-key-9987cb87-6458-4888-b94e-68d9a2da896d", // 콘솔 결제 연동 화면에서 채널 연동 시 생성된 채널 키를 입력해주세요.
            #         paymentId: `payment${crypto.randomUUID()}`,
            #         orderName: "나이키 와플 트레이너 2 SD",
            #         totalAmount: 1000,
            #         currency: "CURRENCY_KRW",
            #         payMethod: "CARD",
            #         customer: {
            #         fullName: "포트원",
            #         phoneNumber: "010-0000-1234",
            #         email: "test@portone.io",
            #         },

                # channelKey: "channel-key-9987cb87-****-****-****-********896d", // 콘솔 결제 연동 화면에서 채널 연동 시 생성된 채널 키를 입력해주세요.
                # customer: {
                # id: "customer-1234", // 고객사에서 관리하는 고객 고유번호
                # },
                # method: {
                # card: {
                #     credential: {
                #     number: "1111111111111111",
                #     expiryMonth: "01",
                #     expiryYear: "20",
                #     birthOrBusinessRegistrationNumber: "900101",
                #     passwordTwoDigits: "00",
                #     },
                # },
                # },
            # },



        # def getTokenApi(path):
        #     API_HOST = "https://api.iamport.kr"
        #     url = API_HOST + path

        #     headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
        #     body = {
        #         "imp_key": "", # REST API Key
        #         "imp_secret": "" # REST API Secret
        #     }
        #     try:
        #         response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
        #         return response
        #     except Exception as ex:
        #          print(
        #     "포트원 토큰 요청 에러\n/payment/views.py/getTokenApi(path) - 78번째 줄 에러 발생"
        #     )

        #     res=getTokenApi("/users/getToken")  # API call
        #     json_object=json.loads(res.text)    # json 객체로 변환
        #     TokenVal = json_object['response']['access_token'] # 토큰값 파싱

        #     print(TokenVal)
# 카카오페이
@csrf_exempt
def kakao_payment(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    first_cart =  cart[0].product.product_name
    remaining_cart_count = len(cart)-1

    if remaining_cart_count > 0:
        orderName = f"{first_cart} 외 {remaining_cart_count}건"
    elif remaining_cart_count == 0:
        orderName = first_cart
    else:
        raise ValueError('카트가 비어있습니다.')

    print(request.method)
    storeId=os.getenv("storeId")
    channelKey=os.getenv("channelKey")

    context={
        "storeId":storeId,
        "channelKey":channelKey,
        "cart": cart,
        "orderName": orderName
    }
    return render(request, "payment/portone_kakao.html",context)

@transaction.atomic
@csrf_exempt
def handle_kakao_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        payment_id = data.get('paymentId')
        user = request.user
        current_time = timezone.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # payment_id DB에 저장
        payment = Payment.objects.create(
            pay_date = formatted_time,
            payment_uuid = payment_id, # 결제uuid 결제취소 시 사용
            pay_method = "kakaoPay",
            #******** 결제예정금액으로 업데이트 예정 ********
            pay_total_price = 80000, 
            pay_confirm = True,
            user=request.user
            )  # 마지막 카트 아이디 설정
        payment.save()
        
        
        # 주문번호 - 매일초기화
        # YYMMDD(6자리)+분류(1자리)+업무절차 코드(3자리)
        # 시간(6)
        # 분류(1) category_id / 카트수량
        # 업무절차(4) 처리프로세스(1) + order_id(3)
        # 1 처리중
        # 2 처리완료
        # 3 취소/오류

        # order테이블에 cart저장
        cart = Cart.objects.filter(user=user)
        payment = Payment.objects.filter(user=user).last()

        order = Order.objects.create(
            user = user,
            product = cart[0].product,
            payment = payment,
            amount = cart[0].amount,
            total_price = cart[0].total_price,
            payment_total_price = payment.pay_total_price,
            order_date = current_time)
        
        code_current_date = current_time.strftime("%y%m%d")
        code_cart_count = len(cart)
        # 업무절차 코드 생성 (2는 고정, order_id는 3자리로 변환)
        process_code = f"2{str(order.id).zfill(3)}"
        
        # 주문번호 생성 및 업데이트
        order_number = f"{code_current_date}{code_cart_count}{process_code}"
      
        order.order_number = int(order_number)
        order.save()

        # 카트 비어있다면
        # 카트 1개
        # 카트 여러개
        for one in cart: 
            product_id = one.product
            category = one.product.category.category_name
            order_items = OrderItems.objects.create(
                user=user,
                order = order,
                product = product_id,
                category = category,
                amount = one.amount,
                total_price = one.total_price,
            )
            order_items.save()

        # # 주문 생성 후 카트 비우기
        cart.delete()   
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


   


# tossPay API 연결
@csrf_exempt
def toss_payment(request):
    if request.method == "POST":
        # URL 설정
        url = "https://pay.toss.im/api/v2/payments"

        # 요청 헤더 설정
        headers = {
            "Content-Type": "application/json"
        }

        # POST 요청에 필요한 JSON 데이터
        data = {
            "orderNo": order_no,
            "amount": 30,
            "amountTaxFree": 0,
            "productDesc": "테스트결제",
            # 발급받은 api키로 교체해야됨(사업자) / 현재는 testapi키
            "apiKey": "sk_test_w5lNQylNqa5lNQe013Nq",
            "autoExecute": True,
            "resultCallback": "https://your-site.com/callback",
            "callbackVersion": "V2",
            # 실제외부 AWS로 연결이 된 url
            "retUrl": "http://your-site.com/ORDER-CHECK?orderno=1",
            "retCancelUrl": "http://your-site.com/close"
        }

        # POST 요청 보내기
        response = requests.post(url, headers=headers, json=data)

         # 응답에서 redirectUrl 추출
        response_data = response.json()
        # 데이터 확인용
        print("response_data ", response_data)
        redirect_url = response_data.get("checkoutPage")
        # url데이터 확인용 
        print("redirect_url, ", redirect_url)

        # redirectUrl로 리다이렉트
        if redirect_url:
            return redirect(redirect_url)
        else:
            # URL이 없을 경우 에러 처리
            return render(request, 'payment/toss_error.html', {'error': '결제 페이지로 리다이렉트할 수 없습니다.'})

    return render(request, 'payment/toss_error.html', {'error': '잘못된 요청입니다.'})

# 결제완료페이가 있고 결제가 됐을 때 DB로 order테이블로 연결
# 주문번호 - 매일초기화
# YYMMDD(6자리)+분류(1자리)+업무절차 코드(3자리)
# 시간(6)
# 분류(1) category_id
# 업무절차(3) 상품 id + order_id