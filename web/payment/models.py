from django.db import models

# Create your models here.

# payment모델
# pay_code // 일련번호 관리
# odr_code // 주문번호
# pay_method // 결제방식 kakao/toss/portone
# pay_date // 결제일
# pay_tot_price // 결제금액
# pay_rest_price // 미지급금
# pay_nobank_user // 입금자명(무통장)
# pay_nobank // 입금은행

class ReadyRequest(models.Model):
    cid = models.CharField(max_length=255)
    partner_order_id = models.CharField(max_length=255)
    partner_user_id = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    total_amount = models.IntegerField()
    tax_free_amount = models.IntegerField()
    vat_amount = models.IntegerField()
    approval_url = models.URLField()
    cancel_url = models.URLField()
    fail_url = models.URLField()

class ApproveRequest(models.Model):
    cid = models.CharField(max_length=255)
    tid = models.CharField(max_length=255)
    partner_order_id = models.CharField(max_length=255)
    partner_user_id = models.CharField(max_length=255)
    pg_token = models.CharField(max_length=255)

class ReadyResponse(models.Model):
    tid = models.CharField(max_length=255)
    tms_result = models.BooleanField()
    created_at = models.DateTimeField()
    next_redirect_pc_url = models.URLField()
    next_redirect_mobile_url = models.URLField()
    next_redirect_app_url = models.URLField()
    android_app_scheme = models.CharField(max_length=255)
    ios_app_scheme = models.CharField(max_length=255)