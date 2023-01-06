import os
from pathlib import Path
from typing import Dict

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = True
ALLOWED_HOSTS = ["*"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
LANGUAGE_CODE = "en-us"
ROOT_URLCONF = "todo.urls"
SERVER_EMAIL = "no-reply@example.com"
DEFAULT_FROM_EMAIL = SERVER_EMAIL
SITE_ID = 1
STATIC_URL = "static/"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
WSGI_APPLICATION = "todo.wsgi.application"

validators_prefix = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{validators_prefix}.UserAttributeSimilarityValidator"},
    {"NAME": f"{validators_prefix}.MinimumLengthValidator"},
    {"NAME": f"{validators_prefix}.CommonPasswordValidator"},
    {"NAME": f"{validators_prefix}.NumericPasswordValidator"},
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",  # allauth
    "django.contrib.staticfiles",
    # local
    "api.apps.ApiConfig",
    "drf_spectacular",
    "todos.apps.TodosConfig",
    # third-party,
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # "corsheaders",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "todo.middleware.debug_middleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# THIRD-PARTY #
# allauth

# corsheaders
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = os.environ["CORS_ALLOWED_ORIGINS"].split(",")

# rest_framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# drf_spectacular
SPECTACULAR_SETTINGS: Dict[str, any] = {
    "COMPONENT_NO_READ_ONLY_REQUIRED": True,  # fix: dart client requires 'token' field
    "COMPONENT_SPLIT_REQUEST": True,  # fix dart client authtoken
    "TITLE": "Todo List API",
    "DESCRIPTION": "A basic todo list API.",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVERS": ["http://192.168.1.100:8001"],
}
