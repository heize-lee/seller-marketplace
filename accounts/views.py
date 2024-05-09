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
# password_change
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordChangeView as AuthPasswordChangeView)
from accounts.forms import PasswordChangeForm  # 커스텀 폼 임포트
# delete_account
from django.contrib.auth import authenticate, login, logout
from .forms import DeleteAccountForm
from .models import UserRegistrationHistory
from django.db import transaction
# login - added remeberme
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm  # 커스텀 로그인 폼 임포트

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)  # 폼에서 처리

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                if remember_me:
                    request.session.set_expiry(1209600)  # 2주
                else:
                    request.session.set_expiry(0)  # 브라우저 종료 시 세션 만료

                next_url = request.GET.get('next')
                return redirect(next_url) if next_url else redirect('home')
        else:
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginForm()  # GET 요청 시 폼 인스턴스 생성
    return render(request, 'accounts/login.html', {'form': form})

# accounts/views.py

from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import DeleteAccountForm

# delete_account
@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(request, username=request.user.email, password=password)
            if user is not None:
                # Delete the user
                user.delete()

                # Logout the user
                logout(request)

                return redirect('delete_account_done')
            else:
                # 비밀번호가 일치하지 않는 경우 오류 메시지 표시
                form.add_error('password', '비밀번호가 일치하지 않습니다.')
    else:
        form = DeleteAccountForm()
    
    return render(request, 'accounts/delete_account.html', {'form': form})

def delete_account_done(request):
    return redirect('delete_account_done')

# delete_account - 3차, 회원탈퇴 후 로그
# @login_required
# def delete_account(request):
#     if request.method == 'POST':
#         form = DeleteAccountForm(request.POST)
#         if form.is_valid():
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=request.user.email, password=password)
#             if user is not None:
#                 with transaction.atomic():
#                     # Save any related objects before deleting the user
#                     # For example, UserRegistrationHistory
#                     # registration_history = UserRegistrationHistory.objects.create(user=user)

#                     # Delete the user
#                     user.delete()

#                     # Logout the user
#                     logout(request)

#                 return redirect('delete_account_done')
#             else:
#                 # 비밀번호가 일치하지 않는 경우 오류 메시지 표시
#                 form.add_error('password', '비밀번호가 일치하지 않습니다.')
#     else:
#         form = DeleteAccountForm()
    
#     return render(request, 'accounts/delete_account.html', {'form': form})

# def delete_account_done(request):
#     # return render(request, 'accounts/delete_account_done.html')
#     return redirect('delete_account_done')

# password_change
class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy('password_change')
    template_name = 'accounts/password_change_form.html'  # 템플릿 위치 재정의
    form_class = PasswordChangeForm  # 커스텀 폼 지정

    def form_valid(self, form):  # 유효성 검사 성공 이후 로직 입력
        messages.success(self.request, '암호를 변경했습니다.')  # 성공 메시지
        return super().form_valid(form)  # 폼 검사 결과를 리턴해야한다.

password_change = PasswordChangeView.as_view()

# account_settings
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