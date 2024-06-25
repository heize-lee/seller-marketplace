from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수 항목입니다.')
        if not phone_number:
            raise ValueError('휴대폰 번호는 필수 항목입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email=email, password=password, phone_number=phone_number, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        BUYER = 'buyer', _('구매자')
        SELLER = 'seller', _('판매자')
        ADMIN = 'admin', _('운영자')

    email = models.EmailField(_('이메일 주소'), unique=True)
    nickname = models.CharField(_('닉네임'), max_length=150, blank=True)
    phone_number = PhoneNumberField(unique=True, blank=False)
    profile_picture = models.ImageField(
        _('프로필 사진'), 
        upload_to='profile_images/%Y/%m/%d/', 
        null=True, 
        blank=True,
        default='profile_images/default/profile_picture.png'
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
    REQUIRED_FIELDS = ['phone_number', 'role']

    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = 'profile_images/default/profile_picture.png'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

# 배송지 모델
class DeliveryAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    recipient = models.CharField(max_length=20) # 수령인
    phone_number = PhoneNumberField(unique=True, blank=False) # 휴대폰
    destination = models.CharField(max_length=50)  # 배송지명
    postal_code = models.CharField(max_length=5)  # 우편번호
    address = models.CharField(max_length=100)  # 주소
    detail_address = models.CharField(max_length=100)  # 상세주소
    is_default = models.BooleanField(default=False)  # 기본배송지 설정 여부

