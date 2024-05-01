# account/views.py
# Version: 1.0
# Date: 2024-04-30

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 로그인 성공 후 리디렉션할 페이지
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)  # 파일을 처리하기 위해 request.FILES를 추가해야 함
        if form.is_valid():
            form.save()  # 폼이 유효하면 데이터를 저장
            return redirect('home')  # 회원가입 완료 페이지로 리디렉션
    else:
        form = SignUpForm()  # GET 요청 시에는 빈 폼을 생성하여 전달
    return render(request, 'accounts/register.html', {'form': form})

def signup_done_view(request):
    return render(request, 'accounts/register_done.html')

def home_view(request):
    return render(request, 'home.html')  # home.html 템플릿을 렌더링합니다.

###

def logout_view(request):
    logout(request)
    return redirect('login')  # 로그아웃 후 리디렉션할 로그인 페이지 경로