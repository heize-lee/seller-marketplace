from allauth.account.views import SignupView
from django.urls import reverse_lazy

class CustomSignupView(SignupView):
    template_name = 'accounts/signup.html'

# URL 패턴에 이 뷰를 연결해야 합니다.
