
# forms.py

from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError




class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    nickname = forms.CharField(max_length=150, required=False, help_text='Optional. Enter your nickname.')  # 닉네임 필드 추가
    phone_number = forms.CharField(max_length=20, help_text='Required. Enter your phone number.')
    profile_picture = forms.ImageField(required=False, help_text='Optional. Upload your profile picture.')  # 프로필 사진 필드 추가
    is_agree_terms = forms.BooleanField(required=False, help_text='Required. Agree to the Terms of Use.')  # 이용 약관 동의 필드 추가
    is_agree_privacy_policy = forms.BooleanField(required=False, help_text='Required. Agree to the Privacy Policy.')  # 개인정보 처리방침 동의 필드 추가

    class Meta:
        model = CustomUser
        fields = ['email', 'nickname', 'phone_number', 'profile_picture', 'is_agree_terms', 'is_agree_privacy_policy']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('This field is required.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    # 휴대폰 번호의 유효성을 검사하고 중복 확인하는 clean_phone_number 메서드
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('This field is required.')

        # 휴대폰 번호의 유효성을 검사합니다.
        if not phone_number.isdigit() or len(phone_number) != 11:
            raise ValidationError("Invalid phone number. Phone number must be 11 digits long and contain only numbers.")
        
        # 이미 사용 중인 휴대폰 번호인지 확인합니다.
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('This phone number is already in use.')
        return phone_number
    

# 추후구현

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['profile_picture']  # 프로필 사진 필드만 사용

#     def clean_profile_picture(self):
#         profile_picture = self.cleaned_data.get('profile_picture')
#         # 프로필 사진이 있는지 확인
#         if not profile_picture:
#             raise forms.ValidationError('Please upload a profile picture.')
#         # 프로필 사진의 유효성 검사 및 파일 형식 확인 등 추가적인 처리
#         # 예를 들어, 이미지 파일 형식인지 확인하는 코드를 추가할 수 있습니다.
#         return profile_picture