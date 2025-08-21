from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = os.get_env("ALLOWED_HOSTS", "").split(",") if os.get_env("ALLOWED_HOSTS") else []

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = os.get_env("CSRF_TRUSTED_ORIGINS", "").split(",") if os.get_env("CSRF_TRUSTED_ORIGINS") else []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ecommerce",
        "USER": os.getenv('POSTGRES_USER', 'postgres'),
        "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Basic secure defaults (expand later)
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = bool(int(os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "0")))
SECURE_HSTS_PRELOAD = bool(int(os.environ.get("SECURE_HSTS_PRELOAD", "0")))
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
