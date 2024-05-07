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
from django.contrib.auth.views import (
    PasswordChangeView as AuthPasswordChangeView
)
from accounts.forms import PasswordChangeForm  # 커스텀 폼 임포트

# delete_account
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import DeleteAccountForm
from .models import UserRegistrationHistory

from django.db import transaction

@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(request, username=request.user.email, password=password)
            if user is not None:
                with transaction.atomic():
                    # Save any related objects before deleting the user
                    # For example, UserRegistrationHistory
                    registration_history = UserRegistrationHistory.objects.create(user=user)

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


# def delete_account(request):
#     if request.method == 'POST':
#         form = DeleteAccountForm(request.POST)
#         if form.is_valid():
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=request.user.email, password=password)
#             if user is not None:
#                 # 비밀번호 일치하는 경우 회원 탈퇴 처리
#                 user.delete()
                
#                 # 사용자의 회원 가입 이력 생성
#                 registration_history = UserRegistrationHistory.objects.create(user=user)

#                 # 로그아웃 후 delete_account_done 페이지로 리다이렉트
#                 logout(request)
#                 return redirect('delete_account_done')
#             else:
#                 # 비밀번호가 일치하지 않는 경우 오류 메시지 표시
#                 form.add_error('password', '비밀번호가 일치하지 않습니다.')
#     else:
#         form = DeleteAccountForm()
    
#     return render(request, 'accounts/delete_account.html', {'form': form})



# @login_required
# def delete_account(request):
#     if request.method == 'POST':
#         form = DeleteAccountForm(request.POST)
#         if form.is_valid():
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=request.user.email, password=password)  # 이메일을 사용자 식별자로 사용
#             if user is not None:
#                 # 비밀번호 일치하는 경우 회원 탈퇴 처리
#                 registration_history = UserRegistrationHistory.objects.create(user=user)  # 사용자의 회원 가입 이력 생성
#                 user.delete()
#                 # 로그아웃 후 delete_account_done 페이지로 리다이렉트
#                 logout(request)
#                 return redirect('delete_account_done')
#             else:
#                 # 비밀번호가 일치하지 않는 경우 오류 메시지 표시
#                 form.add_error('password', '비밀번호가 일치하지 않습니다.')
#     else:
#         form = DeleteAccountForm()
    
#     return render(request, 'accounts/delete_account.html', {'form': form})


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from .forms import DeleteAccountForm

# @login_required
# def delete_account(request):
#     if request.method == 'POST':
#         form = DeleteAccountForm(request.POST)
#         if form.is_valid():
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=request.user.email, password=password)  # username 대신 email 사용
#             if user is not None:
#                 # 비밀번호 일치하는 경우 회원 탈퇴 처리
#                 user.delete()
#                 # 로그아웃 후 delete_account_done 페이지로 리다이렉트
#                 logout(request)
#                 return redirect('delete_account_done')
#             else:
#                 # 비밀번호가 일치하지 않는 경우 오류 메시지 표시
#                 form.add_error('password', '비밀번호가 일치하지 않습니다.')
#     else:
#         form = DeleteAccountForm()
    
#     return render(request, 'accounts/delete_account.html', {'form': form})

# # views.py
# from .models import UserRegistrationHistory

# @login_required
# def delete_account(request):
#     if request.method == 'POST':
#         # 회원 탈퇴 요청을 받았을 때
#         user = request.user
#         # 사용자의 회원 가입 이력 생성
#         registration_history = UserRegistrationHistory.objects.create(user=user)
#         # 사용자 비활성화
#         user.is_active = False
#         user.save()
#         # 로그아웃 후 홈페이지로 리다이렉트
#         logout(request)
#         return redirect('delete_account_done')
#     return render(request, 'accounts/delete_account.html')

def delete_account_done(request):
    return render(request, 'accounts/delete_account_done.html')


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

# login
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return render(request, 'home.html')  # 로그인 성공 시 리다이렉트
#         else:
#             return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'accounts/login.html')


# login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 로그인 이전에 요청한 URL 가져오기
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')  # 또는 return redirect('/')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    
    # GET 요청 시 로그인 페이지 렌더링
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