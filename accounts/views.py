# account/views.py
# Version: 1.0
# Date: 2024-04-30

from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView





###

# from django.contrib.auth import logout

# from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib.auth.forms import AuthenticationForm

# from django.contrib.auth import authenticate, login


# class CustomLoginView(LoginView):
#     template_name = 'accounts/login.html'  # 로그인 템플릿 경로를 지정합니다.

# class CustomLogoutView(LogoutView):
#     template_name = 'accounts/logout.html'  # 로그아웃 템플릿 경로를 지정합니다.



# # login
# class CustomLoginView(LoginView):
#     form_class = AuthenticationForm
#     template_name = 'accounts/login.html'

# accounts/views.py
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'home.html')  # 로그인 성공 시 리다이렉트
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')








class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')
    
    def form_valid(self, form):
        # 이 메서드를 사용하여 유효한 폼을 제출할 때 수행할 추가 작업을 지정할 수 있습니다.
        # 여기에서는 기본 동작을 유지하고 성공 URL로 리디렉션합니다.
        return super().form_valid(form)

# register
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)  # 파일을 처리하기 위해 request.FILES를 추가해야 함
        if form.is_valid():
            form.save()  # 폼이 유효하면 데이터를 저장
            return redirect('home')  # 회원가입 완료 페이지로 리디렉션
    else:
        form = SignUpForm()  # GET 요청 시에는 빈 폼을 생성하여 전달
    return render(request, 'accounts/register.html', {'form': form})

# register_done
def signup_done_view(request):
    return render(request, 'accounts/register_done.html')

# home-test
def home_view(request):
    return render(request, 'home.html')  # home.html 템플릿을 렌더링합니다.