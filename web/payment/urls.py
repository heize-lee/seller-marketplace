from django.urls import path
from .views import toss_payment, kakao_payment, portone_payment, billings, ReadyView, ApproveView, CancelView, FailView

app_name = 'payment'

urlpatterns = [
    path('toss_process/', toss_payment, name='toss_payment'),
    path('kakao_process/', kakao_payment, name='kakao_payment'),
    path('portone_process/', portone_payment, name='portone_payment'),
    path('billings/', billings, name='billings'),
    
    path('ready/<str:agent>/<str:open_type>/', ReadyView.as_view(), name='ready'),
    path('approve/<str:agent>/<str:open_type>/', ApproveView.as_view(), name='approve'),
    path('cancel/<str:agent>/<str:open_type>/', CancelView.as_view(), name='cancel'),
    path('fail/<str:agent>/<str:open_type>/', FailView.as_view(), name='fail'),
]