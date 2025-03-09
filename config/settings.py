from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "https://farbesh.vercel.app/",
    "https://farbesh-tau.vercel.app/",
    "https://farbesh.up.railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "https://farbesh.vercel.app/",
    "https://farbesh-tau.vercel.app/",
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


CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
] 

CORS_ALLOW_HEADERS = [
    "Content-Type",
    "Authorization",
    "X-CSRFToken",
]


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
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',    
    'app',
    'drivers_admin',
]



AUTHENTICATION_BACKENDS = [
    'app.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "optional"



SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"



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
        'PASSWORD': 'rCYzchCYrDASnkehkZySMAHXTEzyYUQE',  # Database password
        'HOST': 'shuttle.proxy.rlwy.net',  # Database host
        'PORT': '38457',  # Database port
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'




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
        'rest_framework_simplejwt.authentication.JWTAuthentication',
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


from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,  
}

REST_USE_JWT = True
