# account/views.py
# Version: 1.0
# Date: 2024-04-30

# register
from django.shortcuts import render, redirect
from .forms import SignUpForm

# login
from django.contrib.auth import authenticate, login

# account_setting (mypage?)
from django.contrib.auth.decorators import login_required

# account_setting - profile
from .forms import ProfileUpdateForm

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ProfileUpdateForm
# from .forms import ProfileUpdateForm, CustomPasswordResetForm  # 가정한 폼

@login_required
def account_settings(request):
    if request.method == 'POST':
        # 폼 인스턴스 생성
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:account_settings')

        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password has been updated!')
            return redirect('accounts:account_settings')

    else:
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    
    context = {
        'profile_form': profile_form,
        'password_form': password_form
    }
    return render(request, 'accounts/account_settings.html', context)





# # password
# from django.urls import reverse_lazy
# from django.contrib.auth.views import PasswordChangeView

# class CustomPasswordChangeView(PasswordChangeView):
#     success_url = reverse_lazy('password_change_done')
    
#     def form_valid(self, form):
#         # 이 메서드를 사용하여 유효한 폼을 제출할 때 수행할 추가 작업을 지정할 수 있습니다.
#         # 여기에서는 기본 동작을 유지하고 성공 URL로 리디렉션합니다.
#         return super().form_valid(form)


# # 잠깐
# @login_required
# def account_settings(request):
#     return render(request, 'accounts/account_settings.html')

# login
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