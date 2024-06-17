from allauth.account.views import SignupView, LoginView
from django.urls import reverse_lazy

# 마이페이지
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# 마이페이지 
@login_required
def mypage_nav(request):
    return render(request, 'accounts/mypage_nav.html')

@login_required
def mypage_section(request, section):
    return render(request, 'accounts/mypage_section.html', {'section': section})

# 로그인
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"  

# 회원가입
class CustomSignupView(SignupView):
    template_name = 'accounts/signup.html'