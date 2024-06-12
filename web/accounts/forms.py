from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser

class CustomSignupForm(SignupForm):
    nickname = forms.CharField(max_length=150, label='닉네임', required=True)
    phone_number = forms.CharField(max_length=15, label='전화번호', required=True)
    is_agree_terms = forms.BooleanField(label='이용 약관 동의', required=True)
    is_agree_privacy_policy = forms.BooleanField(label='개인정보 처리방침 동의', required=True)
    profile_picture = forms.ImageField(label='프로필 사진', required=False)

    def signup(self, request, user):
        user.nickname = self.cleaned_data['nickname']
        user.phone_number = self.cleaned_data['phone_number']
        user.is_agree_terms = self.cleaned_data['is_agree_terms']
        user.is_agree_privacy_policy = self.cleaned_data['is_agree_privacy_policy']
        user.profile_picture = self.cleaned_data.get('profile_picture')
        user.save()
        return user
