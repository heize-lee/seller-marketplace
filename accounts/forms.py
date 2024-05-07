
# accounts/forms.py
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm
from django.core.exceptions import ValidationError

# delete_account
class DeleteAccountForm(forms.Form):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)


# password_change
class PasswordChangeForm(AuthPasswordChangeForm):
    # clean_new_password2 재정의 시에는 super()함수 호출이 필요하다. (부모에 존재하는 유효성 검사이다.)
    def clean_new_password1(self):
        # new_password1에 대한 유효성 검사를 추가로 정의한다.
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')

        if old_password and new_password1:
            if old_password == new_password1:  # 기존 암호와 같을 경우 폼 에러를 일으킨다.
                raise forms.ValidationError('새로운 암호는 기존 암호와 다르게 입력해주세요')
        return new_password1


# profile
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'nickname', 'phone_number', 'profile_picture']

# register
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    nickname = forms.CharField(max_length=150, required=False, help_text='Optional. Enter your nickname.')  # 닉네임 필드 추가
    phone_number = forms.CharField(max_length=20, help_text='Required. Enter your phone number.')
    profile_picture = forms.ImageField(required=False, help_text='Optional. Upload your profile picture.')  # 프로필 사진 필드 추가
    is_agree_terms = forms.BooleanField(required=False, help_text='Required. Agree to the Terms of Use.')  # 이용 약관 동의 필드 추가
    is_agree_privacy_policy = forms.BooleanField(required=False, help_text='Required. Agree to the Privacy Policy.')  # 개인정보 처리방침 동의 필드 추가

    # 바이어와 셀러를 선택할 수 있는 필드 추가
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, help_text='Required. Select your role.')

    def save(self, commit=True):
        user_instance = super().save(commit=False)
        user_instance.role = self.cleaned_data['role']  # 폼에서 선택한 역할을 user의 role 필드에 저장합니다.
        if commit:
            user_instance.save()
        return user_instance

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