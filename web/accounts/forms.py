from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    nickname = forms.CharField(max_length=150, label='닉네임', required=True)
    phone_number = forms.CharField(max_length=15, label='전화번호', required=True)
    is_agree_terms = forms.BooleanField(label='이용 약관 동의', required=True)
    is_agree_privacy_policy = forms.BooleanField(label='개인정보 처리방침 동의', required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.nickname = self.cleaned_data['nickname']
        user.phone_number = self.cleaned_data['phone_number']
        user.is_agree_terms = self.cleaned_data['is_agree_terms']
        user.is_agree_privacy_policy = self.cleaned_data['is_agree_privacy_policy']
        user.save()
        return user
