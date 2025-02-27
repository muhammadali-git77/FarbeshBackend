from pathlib import Path
from datetime import timedelta
import dj_database_url  # PostgreSQL URL bilan ishlash uchun
import os

BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "https://farbesh.up.railway.app",
]

CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "None"  


if os.getenv("DJANGO_ENV") == "production":
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
else:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False



CORS_ALLOW_CREDENTIALS = True  # Cookie va sessionlarni ishlatish uchun
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]  # Ruxsat berilgan HTTP metodlar

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
]  # Frontend so‘rovlarida ishlatilishi mumkin bo‘lgan headerlar


SECRET_KEY = 'django-insecure-^a-7_ke^p@iwzlr)b!$$8%aw)5z0ipp6z@ne4$l#6#n=yng_ow'
DEBUG = True
ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_filters',

    'requests',
    'rest_framework',
    'rest_framework.authtoken',

    'corsheaders',

    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    'app',
    'drivers_admin',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

WSGI_APPLICATION = 'config.wsgi.application'

# PostgreSQL Database
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',  # Database name
        'USER': 'postgres',  # Database user
        'PASSWORD': 'JdGzhLKwIhMlnrtxSMGeRdzKvrlvGbDB',  # Database password
        'HOST': 'turntable.proxy.rlwy.net',  # Database host
        'PORT': '11187',  # Database port
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / "db.sqlite3",
#     }
# }




AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

STATIC_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDA_ROOT = BASE_DIR / 'media'

ACCOUNT_EMAIL_VERIFICATION = "optional"  # Email berish mumkin, lekin tasdiqlash shart emas
ACCOUNT_EMAIL_REQUIRED = True


SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
