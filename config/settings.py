"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
superuser 아이디 pc 비밀번호 1
"""

from pathlib import Path
import os



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'secret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'accounts', # 커스텀 앱을 먼저 로드
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'seller_product',
    'order',  

    # merge-mhs ***확인
    # 'product',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',    # static
                # 'accounts.context_processors.navbar_login_form',    # 추가한 컨텍스트 프로세서
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'



# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# 공용 DB
# env
from dotenv import load_dotenv
load_dotenv()
db_key = os.getenv("DB_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seller_marketplace', # db name
        'USER': 'postgres',
        'PASSWORD': db_key,
        'HOST': 'hanslab.org',  # 또는 PostgreSQL 서버의 IP 주소
        'PORT': '25432',       # PostgreSQL의 기본 포트 번호
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# style.css
STATIC_URL = '/static/'
# 정적 파일이 저장될 폴더 지정 (선택적, 배포 시 중요)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# 개발 중에는 다음과 같이 설정할 수 있습니다.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# profile_picture
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'_media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django.contrib.auth
LOGIN_URL = '/accounts/login/'  # login
LOGIN_REDIRECT_URL = '/'  # 로그인 후 리다이렉션할 URL

LOGOUT_URL = '/accounts/logout/'  # logout
LOGOUT_REDIRECT_URL = '/'

# user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# login
AUTHENTICATION_FORM = 'accounts.forms.LoginForm'