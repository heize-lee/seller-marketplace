
# models.py
# Version: 1.0
# Date: 2024-04-30

# 파일명: models.py
# 생성 날짜: 2024-04-30

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# delete_account-
class UserRegistrationHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    withdrawal_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"User: {self.user.email}, Registration Date: {self.registration_date}, Withdrawal Date: {self.withdrawal_date}"

class CustomUserManager(BaseUserManager):
    """
    사용자 계정을 생성하고 관리하는 매니저 클래스입니다.
    """
    def create_user(self, email, password, role, **extra_fields):
        """
        이메일, 비밀번호, 역할을 기반으로 사용자를 생성하고 저장합니다.
        """
        if not email:
            raise ValueError('이메일은 필수 항목입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        이메일과 비밀번호를 사용하여 슈퍼유저를 생성하고 저장합니다.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Ensure default role is 'admin' for superusers

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    추가적인 속성을 포함한 사용자 정의 사용자 모델입니다.
    """
    class UserType(models.TextChoices):
        BUYER = 'buyer', _('구매자')
        SELLER = 'seller', _('판매자')
        ADMIN = 'admin', _('운영자')

    email = models.EmailField(_('이메일 주소'), unique=True)
    nickname = models.CharField(_('닉네임'), max_length=150, blank=True)
    phone_number = models.CharField(_('전화번호'), max_length=15, blank=True)
    profile_picture = models.ImageField(_('프로필 사진'), upload_to='profile_pics/', null=True, blank=True)
    is_agree_terms = models.BooleanField(_('이용 약관 동의'), default=False)
    is_agree_privacy_policy = models.BooleanField(_('개인정보 처리방침 동의'), default=False)
    is_active = models.BooleanField(_('활성 상태'), default=True)
    is_staff = models.BooleanField(_('스태프 여부'), default=False)
    role = models.CharField(_('역할'), max_length=10, choices=UserType.choices, default=UserType.BUYER)
    date_joined = models.DateTimeField(_('가입 날짜'), auto_now_add=True)
    updated_at = models.DateTimeField(_('업데이트 날짜'), auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email