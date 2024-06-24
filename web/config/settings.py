from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--rqonay!32o)0=@ac%oa$43phsn*%&muf93no5ue@1j@o$6=ih'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts', # Custom user model app
    'django.contrib.sites', # Required for allauth
    'allauth', 
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.naver',
    'products',
    'orders',
    'reviews',
    'cart',
    'payment',
]

# social login
AUTH_USER_MODEL = 'accounts.CustomUser'
SITE_ID = 5

# Allauth settings
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # 로그아웃 후 리디렉션할 URL 설정
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = 'none'  # 이메일 인증 비활성화
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # 이메일 인증 활성화
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False  # Ensure this is set to False

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'SCOPE': [
            'account_email',
            'profile_nickname'
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'METHOD': 'oauth2',
    }
}

SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "mandatory"
SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_ADAPTER = 'accounts.adapter.CustomSocialAccountAdapter'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# KAKAO_CLIENT_ID = os.getenv('KAKAO_CLIENT_ID')
# KAKAO_CLIENT_SECRET = os.getenv('KAKAO_CLIENT_SECRET')

# SOCIALACCOUNT_PROVIDERS = {
#     'kakao': {
#         'APP': {
#             'client_id': os.getenv('KAKAO_CLIENT_ID'),
#             'secret': os.getenv('KAKAO_CLIENT_SECRET'),
#             'key': ''
#         }    
# }}

# 로컬 개발 환경에서 이메일을 콘솔에 출력
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 사용자 정의 회원가입 폼 설정
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
}
ACCOUNT_SIGNUP_REDIRECT_URL = '/'

# Additional allauth settings to disable username
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

load_dotenv()
db_password = os.getenv("DB_PASSWORD")
DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seller_ljh2',
        'USER': 'postgres',
        'PASSWORD': db_password,
        'HOST': 'db.hanslab.org',  # 또는 PostgreSQL 서버의 IP 주소
        'PORT': '35432',       # PostgreSQL의 기본 포트 번호
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# 정적 파일 URL 경로
STATIC_URL = '/static/'

# 개발 환경에서 사용할 정적 파일 디렉토리
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 운영 환경에서 정적 파일을 모을 디렉토리
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'