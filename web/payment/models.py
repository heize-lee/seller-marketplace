from django.db import models
from products.models import Product
from cart.models import Cart
from django.conf import settings
# Create your models here.

# payment모델
# pay_code // 일련번호 관리
# odr_code // 주문번호
# ----------------------------
# 주문번호 - 매일초기화
# YYMMDD(6자리)+분류(1자리)+업무절차 코드(3자리)
# 시간(6)
# 분류(1) category_id
# 업무절차(3) 상품 id + order_id

# 사과 외 3건
# 주문번호

# 사과 - 주문번호 1
# 2 - 주문번호 2
# 3 - 주문번호 3
# 4 - 주문번호 4

# ----------------------------
# pay_confirm // 결제완료여부 O/X
# pay_method // 결제방식 kakao/toss/portone
# pay_date // 결제일
# pay_tot_price // 결제금액
# pay_rest_price // 미지급금
# pay_nobank_user // 입금자명(무통장)
# pay_nobank // 입금은행

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    payment_uuid = models.CharField(max_length=100, default=True, unique=True)
    pay_method = models.CharField(max_length=25)
    pay_date = models.DateTimeField()
    pay_totoal_price = models.IntegerField()
    pay_nobank_user = models.CharField(max_length=20, blank=True)
    pay_nobank = models.CharField(max_length=50, blank=True)
    pay_confirm = models.BooleanField(default=False)

    

# class ReadyRequest(models.Model):
#     cid = models.CharField(max_length=255)
#     partner_order_id = models.CharField(max_length=255)
#     partner_user_id = models.CharField(max_length=255)
#     item_name = models.CharField(max_length=255)
#     quantity = models.IntegerField()
#     total_amount = models.IntegerField()
#     tax_free_amount = models.IntegerField()
#     vat_amount = models.IntegerField()
#     approval_url = models.URLField()
#     cancel_url = models.URLField()
#     fail_url = models.URLField()

# class ApproveRequest(models.Model):
#     cid = models.CharField(max_length=255)
#     tid = models.CharField(max_length=255)
#     partner_order_id = models.CharField(max_length=255)
#     partner_user_id = models.CharField(max_length=255)
#     pg_token = models.CharField(max_length=255)

# class ReadyResponse(models.Model):
#     tid = models.CharField(max_length=255)
#     tms_result = models.BooleanField()
#     created_at = models.DateTimeField()
#     next_redirect_pc_url = models.URLField()
#     next_redirect_mobile_url = models.URLField()
#     next_redirect_app_url = models.URLField()
#     android_app_scheme = models.CharField(max_length=255)
#     ios_app_scheme = models.CharField(max_length=255)