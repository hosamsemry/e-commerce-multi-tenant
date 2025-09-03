from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "djoser",
    "django.contrib.postgres",

    "apps.tenancy",
    "apps.accounts",
    "apps.marketplace",
    "apps.products",
    "apps.orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.tenancy.middleware.TenantMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"
ASGI_APPLICATION = "project.asgi.application"

DATABASES = {}



LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Cairo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASES_ATOMIC_REQUESTS = True
AUTH_USER_MODEL = "accounts.User"

#Payment
PAYMOB_API_KEY     = os.getenv("PAYMOB_API_KEY")
PAYMOB_HMAC_KEY    = os.getenv("PAYMOB_HMAC_KEY")
PAYMOB_SECRET_KEY  = os.getenv("PAYMOB_SECRET_KEY")
PAYMOB_PUBLIC_KEY  = os.getenv("PAYMOB_PUBLIC_KEY")
PAYMOB_MERCHANT_ID = os.getenv("PAYMOB_MERCHANT_ID")
PAYMOB_INTEGRATION_ID = os.getenv("PAYMOB_INTEGRATION_ID")
PAYMOB_IFRAME_ID  = os.getenv("PAYMOB_IFRAME_ID")
PAYMOB_AUTH_URL = "https://accept.paymobsolutions.com/api/auth/tokens"
PAYMOB_ORDER_URL = "https://accept.paymobsolutions.com/api/ecommerce/orders"
PAYMOB_PAYMENT_KEY_URL= "https://accept.paymobsolutions.com/api/acceptance/payment_keys"

# Celery 
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

#email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


DJOSER = {
    "USER_ID_FIELD": "email",
    "LOGIN_FIELD": "email",
    'SERIALIZERS': {
        'user_create': 'apps.accounts.serializers.UserCreateSerializer',
        "TOKEN_OBTAIN_SERIALIZER": "apps.accounts.serializers.CustomTokenObtainPairSerializer",
        'current_user': 'apps.accounts.serializers.UserSerializer',
        'user': 'apps.accounts.serializers.UserSerializer',
    },
    'PASSWORD_RESET_CONFIRM_RETYPE':True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION':True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
    'SET_USERNAME_RETYPE':True,
    'SET_PASSWORD_RETYPE':True,
    'USERNAME_RESET_CONFIRM_URL':'email/reset/confirm/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'ACTIVATION_URL': 'auth/activate/?uid={uid}&token={token}',
    'PASSWORD_RESET_CONFIRM_URL': 'auth/reset-password/?uid={uid}&token={token}',
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True
}