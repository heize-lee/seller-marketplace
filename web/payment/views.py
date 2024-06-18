from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import uuid
import requests
import json
import os
import dotenv
import urllib.parse

from django.views.decorators.csrf import csrf_exempt
from django.views import View

from .services import SampleService

# Create your views here.
# 카카오페이 java 예제코드 > python
class ReadyView(View):
    def get(self, request, agent, open_type):
        service = SampleService()
        ready_response = service.ready(agent, open_type)

        if agent == "mobile":
            return redirect(ready_response.next_redirect_mobile_url)

        if agent == "app":
            context = {"webviewUrl": f"app://webview?url={ready_response.next_redirect_app_url}"}
            return render(request, 'payment/ready.html', context)

        context = {"response": ready_response}
        return render(request, f"{agent}/{open_type}/ready.html", context)
    
    def post(self, request, agent, open_type):
        service = SampleService()
        ready_response = service.ready(agent, open_type)

        if agent == "mobile":
            return redirect(ready_response.next_redirect_mobile_url)

        if agent == "app":
            context = {"webviewUrl": f"app://webview?url={ready_response.next_redirect_app_url}"}
            return render(request, 'payment/ready.html', context)

        context = {"response": ready_response}
        return render(request, f"{agent}/{open_type}/ready.html", context)

class ApproveView(View):
    def get(self, request, agent, open_type):
        pg_token = request.GET.get("pg_token")
        service = SampleService()
        approve_response = service.approve(pg_token)
        context = {"response": approve_response}
        return render(request, f"{agent}/{open_type}/approve.html", context)

class CancelView(View):
    def get(self, request, agent, open_type):
        return render(request, f"{agent}/{open_type}/cancel.html")

class FailView(View):
    def get(self, request, agent, open_type):
        return render(request, f"{agent}/{open_type}/fail.html")


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
            billing_key=os.getenv("billing_key")
            PORTONE_API_KEY=os.getenv("PORTONE_API_KEY")
            # print(request.method)
            # 고객사에서 채번하는 새로운 결제 ID를 만듭니다.
            payment_id = "test1" # 이 부분은 해당 함수의 Python 구현에 따라 다를 수 있습니다.
            encoded_payment_id = urllib.parse.quote(payment_id)
            # 포트원 빌링키 결제 API 호출
            url = f"https://api.portone.io/payments/{encoded_payment_id}/billing-key"
            headers = {
                "Authorization": f"PortOne {PORTONE_API_KEY}",
                "Content-Type": "application/json",
            }

            # 고객 정보와 요청 바디 구성
            data = {
                "billingKey": billing_key,
                "orderName": "단건결제",
                "customer": {
                    "id": "seller",
            },  # 실제 고객 정보로 채워야 합니다.
                "amount": {
                    "total": 900,
                },
                "currency": "KRW",
            }
            # v2의 API 키 발급 따로 받아야 함
            # '{"type":"INVALID_REQUEST","message":"Invalid value for: body\\nexpected \'\\"\', offset: 0x0000000f, buf:\\n+----------+-------------------------------------------------+------------------+\\n|          |  0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f | 0123456789abcdef |\\n+----------+-------------------------------------------------+------------------+\\n| 00000000 | 7b 22 62 69 6c 6c 69 6e 67 4b 65 79 22 3a 20 6e | {\\"billingKey\\": n |\\n| 00000010 | 75 6c 6c 2c 20 22 6f 72 64 65 72 4e 61 6d 65 22 | ull, \\"orderName\\" |\\n| 00000020 | 3a 20 22 5c 75 63 36 64 34 5c 75 61 63 30 34 20 | : \\"\\\\uc6d4\\\\uac04  |\\n+----------+-------------------------------------------------+------------------+\\nThe original input: {\\"billingKey\\": null, \\"orderName\\": \\"\\\\uc6d4\\\\uac04 \\\\uc774\\\\uc6a9\\\\uad8c \\\\uc815\\\\uae30\\\\uacb0\\\\uc81c\\", \\"customer\\": {\\"id\\": \\"seller\\"}, \\"amount\\": {\\"total\\": 900}, \\"currency\\": \\"KRW\\"}"}'

            response = requests.post(url, headers=headers, json=data)

            # 응답 상태 검사
            if not response.ok:
                raise Exception(f"paymentResponse: {response.status_code} {response.text}")

            # 응답 데이터 출력 또는 추가 처리
            print(response.json())
            return render(request, "payment/portone_done.html")

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
    print(request.method)
    storeId=os.getenv("storeId")
    channelKey=os.getenv("channelKey")
    context={
        "storeId":storeId,
        "channelKey":channelKey
    }
    return render(request, "payment/portone_kakao.html",context)
    if request.method == "POST":
       pass


    #     url = "https://open-api.kakaopay.com/online/v1/payment/ready"
    #     headers = {
    #         'Authorization': "KakaoAK " + "fe83a8063428f1aaa8bde37f101ec1a4",
    #         'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    #     }
    #     params = {
    #         'cid': "TC0ONETIME",
    #         'partner_order_id': order_no,
    #         'partner_user_id': user,
    #         'item_name': '포인트',
    #         'quantity': 1,
    #         'total_amount': 0,
    #         'vat_amount': 200,
    #         'tax_free_amount': 0,
    #         'approval_url': 'http://localhost:8080', # 결제 성공 시 이동 url
    #         'fail_url': 'http://localhost:8080',    # 결제 취소 시 이동 url
    #         'cancel_url': 'http://localhost:8080', # 결제 실패 시 이동 url
    #     }
    #     response = requests.post(url, params=params, headers=headers)
    #     if response.status_code == 200:
    #         response_data = response.json()
    #         next_redirect_pc_url = response_data.get('next_redirect_pc_url')
    #         return redirect(next_redirect_pc_url)
    #     else:
    #         return render(request, 'payment/kakao_error.html', {'error': '카카오페이 결제 준비 중 오류가 발생했습니다.'})
    #     # response = json.loads(response.text)
    #     # return redirect(response) 
    # return render(request, 'orders:order_done.html', )
    
        # POST /online/v1/payment/ready HTTP/1.1
        # Host: open-api.kakaopay.com
        # Authorization: SECRET_KEY ${SECRET_KEY}
        # Content-Type: application/json
        # ####
        # curl --location 'https://open-api.kakaopay.com/online/v1/payment/ready' \
        # --header 'Authorization: SECRET_KEY ${SECRET_KEY}' \
        # --header 'Content-Type: application/json' \
        # --data '{
        #         "cid": "TC0ONETIME",
        #         "partner_order_id": "partner_order_id",
        #         "partner_user_id": "partner_user_id",
        #         "item_name": "초코파이",
        #         "quantity": "1",
        #         "total_amount": "2200",
        #         "vat_amount": "200",
        #         "tax_free_amount": "0",
        #         "approval_url": "https://developers.kakao.com/success",
        #         "fail_url": "https://developers.kakao.com/fail",
        #         "cancel_url": "https://developers.kakao.com/cancel"
        #     }'

@csrf_exempt
def billings(request):
    # 실제 로직은 위에서 billingkey를 발급받고 DB에 저장

    billing_key=request.get("billing_key")
    PORTONE_API_KEY=os.getenv("PORTONE_API_KEY")
    # print(request.method)
    # 고객사에서 채번하는 새로운 결제 ID를 만듭니다.
    payment_id = "test1234" # 이 부분은 해당 함수의 Python 구현에 따라 다를 수 있습니다.
    encoded_payment_id = urllib.parse.quote(payment_id)
    # 포트원 빌링키 결제 API 호출
    url = f"https://api.portone.io/payments/{encoded_payment_id}/billing-key"
    headers = {
        "Authorization": f"PortOne {PORTONE_API_KEY}",
        "Content-Type": "application/json",
    }

    # 고객 정보와 요청 바디 구성
    data = {
        "billingKey": billing_key,
        "orderName": "카카오 단건결제",
        "customer": {
            "id": "hans",
    },  # 실제 고객 정보로 채워야 합니다.
        "amount": {
            "total": 8900,
        },
        "currency": "KRW",
    }
    # v2의 API 키 발급 따로 받아야 함
    # '{"type":"INVALID_REQUEST","message":"Invalid value for: body\\nexpected \'\\"\', offset: 0x0000000f, buf:\\n+----------+-------------------------------------------------+------------------+\\n|          |  0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f | 0123456789abcdef |\\n+----------+-------------------------------------------------+------------------+\\n| 00000000 | 7b 22 62 69 6c 6c 69 6e 67 4b 65 79 22 3a 20 6e | {\\"billingKey\\": n |\\n| 00000010 | 75 6c 6c 2c 20 22 6f 72 64 65 72 4e 61 6d 65 22 | ull, \\"orderName\\" |\\n| 00000020 | 3a 20 22 5c 75 63 36 64 34 5c 75 61 63 30 34 20 | : \\"\\\\uc6d4\\\\uac04  |\\n+----------+-------------------------------------------------+------------------+\\nThe original input: {\\"billingKey\\": null, \\"orderName\\": \\"\\\\uc6d4\\\\uac04 \\\\uc774\\\\uc6a9\\\\uad8c \\\\uc815\\\\uae30\\\\uacb0\\\\uc81c\\", \\"customer\\": {\\"id\\": \\"hans\\"}, \\"amount\\": {\\"total\\": 8900}, \\"currency\\": \\"KRW\\"}"}'

    response = requests.post(url, headers=headers, json=data)

    # 응답 상태 검사
    if not response.ok:
        raise Exception(f"paymentResponse: {response.status_code} {response.text}")

    # 응답 데이터 출력 또는 추가 처리
    print(response.json())
    return render(request, "orders/order_done.html")

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