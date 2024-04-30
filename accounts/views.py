# account/views.py
# Version: 1.0
# Date: 2024-04-30

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 회원가입 후 로그인 페이지로 리디렉션
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 로그인 성공 후 리디렉션할 페이지
        else:
            return render(request, 'accounts:login.html', {'error': 'Invalid username or password'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # 로그아웃 후 리디렉션할 로그인 페이지 경로