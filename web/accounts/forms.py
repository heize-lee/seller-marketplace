from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser
import re
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError

# 지현 (회원가입)
class CustomSignupForm(SignupForm):
    nickname = forms.CharField(max_length=150, label='닉네임', required=True)
    # phone_number = forms.CharField(max_length=15, label='전화번호', required=True)
    phone_number = PhoneNumberField(label='전화번호', required=True, region='KR')
    is_agree_terms = forms.BooleanField(label='이용 약관 동의', required=True)
    is_agree_privacy_policy = forms.BooleanField(label='개인정보 처리방침 동의', required=True)
    profile_picture = forms.ImageField(label='프로필 사진', required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('중복된 이메일입니다.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # PhoneNumber 객체를 문자열로 변환
        phone_number_str = str(phone_number)
        if not re.match(r'^\+?\d{10,15}$', phone_number_str):
            raise forms.ValidationError('유효한 전화번호 형식이 아닙니다. 예: +821012341123')
        return phone_number

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError('비밀번호는 최소 8자 이상이어야 합니다.')
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('비밀번호에는 최소 하나의 대문자가 포함되어야 합니다.')
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError('비밀번호에는 최소 하나의 소문자가 포함되어야 합니다.')
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError('비밀번호에는 최소 하나의 숫자가 포함되어야 합니다.')
        if not re.search(r'[\W_]', password):
            raise forms.ValidationError('비밀번호에는 최소 하나의 특수문자가 포함되어야 합니다.')
        return password

    def signup(self, request, user):
        user.nickname = self.cleaned_data['nickname']
        user.phone_number = self.cleaned_data['phone_number']
        user.is_agree_terms = self.cleaned_data['is_agree_terms']
        user.is_agree_privacy_policy = self.cleaned_data['is_agree_privacy_policy']
        user.profile_picture = self.cleaned_data.get('profile_picture')
        user.save()
        return user


# 재웅 (프로필 사진 수정)
# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['nickname', 'phone_number', 'profile_picture']


from django import forms
from .models import CustomUser

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'nickname', 'email', 'phone_number', 'is_agree_terms', 'is_agree_privacy_policy']
