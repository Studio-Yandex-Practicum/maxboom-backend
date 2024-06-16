# flake8: noqa
import os
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv
from yookassa import Configuration

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', "django")

DEBUG = bool(os.getenv('DEBUG', 1))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', "127.0.0.1 localhost").split(' ')


# Application definition

# FIRST_PARTY_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
# ]
#
# THIRD_PARTY_APPS = [
#     'rest_framework',
# ]
#
# LOCAL_APPS = [
#     'accounts',
#     'api',
#     'blog',
#     'catalogue',
#     'core',
#     'news',
#     'payment',
#     'shop_reviews'
# ]
#
# INSTALLED_APPS = FIRST_PARTY_APPS + THIRD_PARTY_APPS + LOCAL_APPS


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_spectacular',
    'corsheaders',
    'accounts.apps.AccountsConfig',
    'api',
    'blog',
    'catalogue',
    'sorl.thumbnail',
    'django_filters',
    'core',
    'news',
    'payment',
    'shop_reviews',
    'stories.apps.StoriesConfig',
    'phonenumber_field',
    'cart',
    'order',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'accounts.middleware.RemoveWwwAuthenticateMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'maxboom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost',
    'http://127.0.0.1',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://www.gealit.ru',
    'https://www.gealit.ru',
    'http://gealit.ru',
    'https://gealit.ru',
]

WSGI_APPLICATION = 'maxboom.wsgi.application'

DATABASES = {
    # SQLite default database settings.
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    # PostgreSQL default database settings.
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django'),
        'USER': os.getenv('POSTGRES_USER', 'django'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'POST': os.getenv('DB_PORT', 5432)
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'collected_static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'rest_framework.authentication.TokenAuthentication',
)

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'EXCEPTION_HANDLER': 'accounts.exceptions.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Maxboom API',
    'DESCRIPTION': 'Maxboom shop',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

DJOSER = {
    'HIDE_USERS': False,
    'LOGIN_FIELD': 'email',
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'api/user-activation/{uid}/{token}',
    # 'SEND_CONFIRMATION_EMAIL': True,
    'USER_AUTHENTICATION_RULE': 'djoser.email',
    'SERIALIZERS': {
        'user_create': 'djoser.serializers.UserCreateSerializer',
        'user': 'djoser.serializers.UserSerializer',
        'current_user': 'api.serializers.accounts_serializers.CurrentUserSerializer',
    },
    'PERMISSIONS': {
        'user_list': ['rest_framework.permissions.AllowAny'],
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'current_user': ['rest_framework.permissions.IsAuthenticated'],
    },
}
# Минимальное количество товара в заказе
MIN_AMOUNT_PRODUCT = 1
# Скидка авторизованного пользователя
DISCOUNT_USER = Decimal('0.5')
DISCOUNT_ANONYM = Decimal('0.8')

# Конфигурация yookassa
Configuration.configure(os.getenv('Y_SHOP_ID'), os.getenv('Y_SECRET_KEY'))

"""
Коды ставок НДС:
КОД	    СТАВКА НДС
1	    Без НДС
2	    НДС по ставке 0%
3	    НДС по ставке 10%
4	    НДС чека по ставке 20%
5	    НДС чека по расчетной ставке 10/110
6	    НДС чека по расчетной ставке 20/120
"""
VAT_CODE = '1'

# WB API
WB_API = os.getenv('AUTHORIZATION')
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
