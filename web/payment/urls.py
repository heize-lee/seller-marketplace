from django.urls import path
from .views import toss_payment, kakao_payment, handle_kakao_payment, portone_payment

app_name = 'payment'

urlpatterns = [
    path('toss_process/', toss_payment, name='toss_payment'),
    path('kakao_process/', kakao_payment, name='kakao_payment'),
    path('portone_process/', portone_payment, name='portone_payment'),
    path('handle_kakao_payment/', handle_kakao_payment, name='handle_kakao_payment'),
    
    
]