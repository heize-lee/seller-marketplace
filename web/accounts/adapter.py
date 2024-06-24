# accounts/adapter.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_field

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = sociallogin.user
        user_email(user, data.get('email') or '')
        user_field(user, 'nickname', data.get('nickname') or '')
        return user

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        if not user.pk:
            extra_data = sociallogin.account.extra_data

            email = extra_data.get('email', '')
            if not email:
                raise ValueError('이메일은 필수 항목입니다.')
            user_email(user, email)

            nickname = extra_data.get('nickname', '')
            if not nickname:
                raise ValueError('닉네임은 필수 항목입니다.')
            user.nickname = nickname

            phone_number = extra_data.get('phone_number', '')
            if not phone_number:
                raise ValueError('휴대폰 번호는 필수 항목입니다.')
            user.phone_number = phone_number

            user.is_agree_terms = True  # 필요에 따라 조정
            user.is_agree_privacy_policy = True  # 필요에 따라 조정
            user.set_unusable_password()
            user.save()
        return user
