"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

import decouple
import dj_database_url
import celery.schedules
from django.utils.translation import gettext_lazy as _

# IMPORTANT: This variable must be changed on each release
# to control the entire project version.
from rest_framework.reverse import reverse_lazy

VERSION = "1.0.3"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Decouple Config
# https://github.com/henriquebastos/python-decouple

config = decouple.AutoConfig(BASE_DIR.parent)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "DJANGO_SECRET_KEY", "9x#)gd&p@@+pb+*4_8maaof-^r&z(&j*w%g80zf3x9yw^uea-2"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DJANGO_DEBUG", True, cast=bool)

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", "*", cast=decouple.Csv())

# Application definition

INSTALLED_APPS = [
    "commons.admin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # Third-part APPs
    "corsheaders",
    "rest_framework",
    "ckeditor",
    # Project APPs
    "apps.domain",
    "apps.admin",
    "apps.api",
    "apps.worker",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # CORS Support.
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Custom Project Middleware
    "commons.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = "urls.production"

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
            "builtins": [
                "commons.templatetags.builtins",
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": config(
        "DATABASE_URL",
        default="postgres://postgres:postgres@localhost:5432/base",
        cast=dj_database_url.parse,
    )
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# The model to use to represent a User.
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-user-model

AUTH_USER_MODEL = "domain.User"

# Superuser Settings

SUPERUSER_NAME = config("DJANGO_SUPERUSER_NAME", default="admin")
SUPERUSER_EMAIL = config("DJANGO_SUPERUSER_EMAIL", default="contato@arturgomes.com.br")
SUPERUSER_PASSWORD = config("DJANGO_SUPERUSER_PASSWORD", default="password123")


# Auto Field
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (("en-us", _("English")), ("pt-br", _("Brazilian Portuguese")))

# Internationalization
# https://docs.djangoproject.com/en/3.2/ref/settings/#locale-paths

LOCALE_PATHS = (BASE_DIR / "locale",)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_DIRS = (BASE_DIR / "assets",)

# Django Rest Framework Settings
# http://www.django-rest-framework.org/

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "commons.djutils.api.pagination.DefaultPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": ("commons.api.auth.ClientAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("commons.api.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "EXCEPTION_HANDLER": "commons.api.handlers.exceptions.exception_handler",
    "NON_FIELD_ERRORS_KEY": "general",
}

# Authentication Client

AUTHENTICATION_CLIENT = "commons.api.jwt_auth.JwtAuthenticationClient"

# JWT Settings
# Use ``python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'``
# to generate a new key.

JWT_KEY = config(
    "JWT_KEY", default="&@_rv-kvpcw-m9aqja3qky*$g0vuuj1_w(ob7!%!zrslrn^bb^"
)
JWT_EXP = config("JWT_EXP", default=3600, cast=int)

# Public API Access
# Define the settings to use ``commons.api.permission.IsPublic`` permission.

PUBLIC_API_ACCESS_KEY = config(
    "PUBLIC_API_ACCESS_KEY",
    default="1t*83=oh2y)!dzi&h%a7&5w%eq%$oldjh$zdj$gpfmgbqzz638",
)

# CORS Settings
# https://github.com/adamchainz/django-cors-headers

CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", False, cast=bool)
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", "", cast=decouple.Csv())

CORS_ALLOW_METHODS = config(
    "CORS_ALLOW_METHODS", "DELETE,GET,OPTIONS,PATCH,POST,PUT", cast=decouple.Csv()
)

CORS_ALLOW_HEADERS = config(
    "CORS_ALLOW_HEADERS",
    "accept,accept-encoding,accept-timezone,authorization,content-type,dnt,origin,"
    "user-agent,x-csrftoken,x-requested-with",
    cast=decouple.Csv(),
)


# Admin Customization
# https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#adminsite-attributes

ADMIN_SITE_TITLE = "Base"  # Admin browser title
ADMIN_SITE_HEADER = "Base"  # Admin header text
ADMIN_SITE_INDEX_TITLE = _("Home")  # Admin index page title
ADMIN_SITE_URL_PREFIX = "/admin/"  # Admin url prefix
ADMIN_SITE_URL = None  # Remove site URL

# Admin Shortcuts

ADMIN_SHORTCUTS = [
    {
        "title": _("Users"),
        "url": reverse_lazy("admin:domain_user_changelist"),
        "icon": {"name": "users"},
    }
]

# Admin User Links

ADMIN_USER_LINKS = [
    {"title": _("Settings"), "url": reverse_lazy("dynamic-config")},
    {"title": _("API Docs"), "url": reverse_lazy("api-docs")},
]

# Email Settings
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-EMAIL_HOST

EMAIL_HOST = config("EMAIL_HOST", default=None)
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = config("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default=None)
EMAIL_PORT = config("EMAIL_PORT", default=587)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# Domain
# Provide ability to generate correct absolute urls in missing request scope.

DOMAIN = config("DOMAIN", "http://localhost:8000/")


# Dynamic Config

DYNAMIC_CONFIG_BACKEND = (
    "apps.crosscutting.dynamic_config.backends.db.DBDynamicConfigBackend"
)
DYNAMIC_CONFIG_MODEL = "domain.DynamicConfigParameter"

DYNAMIC_CONFIG = [
    {
        "name": _("Example settings"),
        "description": _("Just a example of how settings is inside admin."),
        "group": _("Example"),
        "key": "example-settings",
        "required": True,
        "form_field": "django.forms.IntegerField",
        "form_field_widget": "django.contrib.admin.widgets.AdminIntegerFieldWidget",
        "validators": [
            ("django.core.validators.MinValueValidator", {"limit_value": 0})
        ],
        "cast": int,
        "default": 1,
    }
]

# CKEditor Settings
# https://django-ckeditor.readthedocs.io/en/latest/#optional-customizing-ckeditor-editor

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "custom",
        "toolbar_custom": [
            {"name": "styles", "items": ["Format"]},
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "RemoveFormat",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                ],
            },
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
            {"name": "insert", "items": ["Image", "HorizontalRule", "Iframe"]},
            {"name": "tools", "items": ["Maximize"]},
            "/",
            {"name": "tools", "items": ["Source"]},
        ],
    },
    "minimal": {
        "toolbar": "minimal",
        "toolbar_minimal": [
            ["Bold", "Italic", "Underline"],
            ["NumberedList", "BulletedList"],
            ["Link", "Unlink"],
            ["RemoveFormat"],
            ["Maximize"],
        ],
    },
}

# Channels Settings

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}
ADMIN_BASIC_PERMISSIONS = {
    "UserAdmin": ["view"],
}
ADMIN_PERMISSIONS = {}


# Notification

NOTIFICATION_BACKEND = (
    "apps.websocket.notification.backend.console.WSNotificationBackend"
)
NOTIFICATIONS = {}

# Celery Settings
# http://docs.celeryproject.org/en/5.0/configuration.html

CELERY_TIMEZONE = TIME_ZONE

CELERY_TASK_DEFAULT_QUEUE = "base"

CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["application/json"]

CELERY_RESULT_BACKEND = None
CELERY_TASK_SOFT_TIME_LIMIT = 30

CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://:@localhost:6379/0")

CELERY_BEAT_SCHEDULE = {
    "example_task": {
        "task": "example_task",
        "schedule": celery.schedules.crontab(minute="*"),
    }
}
