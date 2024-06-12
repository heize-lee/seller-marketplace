from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class UserRegistrationHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    withdrawal_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"User: {self.user.email}, Registration Date: {self.registration_date}, Withdrawal Date: {self.withdrawal_date}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, role, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수 항목입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        BUYER = 'buyer', _('구매자')
        SELLER = 'seller', _('판매자')
        ADMIN = 'admin', _('운영자')

    email = models.EmailField(_('이메일 주소'), unique=True)
    nickname = models.CharField(_('닉네임'), max_length=150, blank=True)
    phone_number = models.CharField(_('전화번호'), max_length=15, blank=True)
    profile_picture = models.ImageField(
        _('프로필 사진'), 
        upload_to='profile_images/%Y/%m/%d/', 
        null=True, 
        blank=True
    )
    is_agree_terms = models.BooleanField(_('이용 약관 동의'), default=False)
    is_agree_privacy_policy = models.BooleanField(_('개인정보 처리방침 동의'), default=False)
    is_active = models.BooleanField(_('활성 상태'), default=True)
    is_staff = models.BooleanField(_('스태프 여부'), default=False)
    role = models.CharField(_('역할'), max_length=10, choices=UserType.choices, default=UserType.BUYER)
    date_joined = models.DateTimeField(_('가입 날짜'), auto_now_add=True)
    updated_at = models.DateTimeField(_('업데이트 날짜'), auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # 기존 user_set과 충돌 방지
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # 기존 user_set과 충돌 방지
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email
