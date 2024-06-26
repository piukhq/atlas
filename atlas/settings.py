"""
Django settings for atlas project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from environment import env_var, read_env

read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "k@k3(kx+bdm25skdw^&d88+2(5cg@54r6$kqbjyiycsub)-g#("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_var("ATLAS_DEBUG", False)

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "https://*.bink.com",
    "https://*.bink.sh",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_prometheus",
    "rest_framework",
    "prometheus.apps.PrometheusConfig",
    "membership",
    "transactions",
    "ubiquity_users",
    "rangefilter",
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "two_factor",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
    "django_otp.middleware.OTPMiddleware",
]

ROOT_URLCONF = "atlas.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "atlas.wsgi.application"

# Logging
LOG_LEVEL = env_var("LOG_LEVEL", "DEBUG").upper()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "{asctime} | {levelname} | {name}:{funcName}(L{lineno}) | {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default"},
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# So apparently django_prometheus.db.backends.postgresql_psycopg2 is a db engine wrapper
# to get metrics about db queries?

if env_var("ATLAS_DATABASE_URI"):
    DATABASES = {
        "default": dj_database_url.config(
            env="ATLAS_DATABASE_URI",
            conn_max_age=600,
            engine="django.db.backends.postgresql_psycopg2",
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env_var("ATLAS_DATABASE_NAME", "atlas"),
            "USER": env_var("ATLAS_DATABASE_USER", "postgres"),
            "PASSWORD": env_var("ATLAS_DATABASE_PASS"),
            "HOST": env_var("ATLAS_DATABASE_HOST", "postgres"),
            "PORT": env_var("ATLAS_DATABASE_PORT", "5432"),
            "CONN_MAX_AGE": 0,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = "/tmp/static/"
STATIC_URL = env_var("STATIC_URL", "/audit/static/")


AZURE_CONTAINER = env_var("AZURE_CONTAINER")
AZURE_TRANSACTION_BASE_DIRECTORY = env_var("AZURE_TRANSACTION_BASE_DIRECTORY", "scheme")
AZURE_CUSTOM_DOMAIN = env_var("AZURE_CUSTOM_DOMAIN")
BLOB_STORAGE_DSN = env_var("BLOB_STORAGE_DSN")
DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"

DELETED_UBIQUITY_USERS_CONTAINER = env_var("DELETED_UBIQUITY_USERS_CONTAINER")
TRANSACTION_REPORTS_CONTAINER = env_var("TRANSACTION_REPORTS_CONTAINER")

SERVICE_API_KEY = "F616CE5C88744DD52DB628FAD8B3D"
ATLAS_SERVICE_AUTH_HEADER = "Token {}".format(SERVICE_API_KEY)

# AMQP connection details
AMQP_USER = env_var("AMQP_USER", "guest")
AMQP_PASSWORD = env_var("AMQP_PASSWORD", "guest")
AMQP_HOST = env_var("AMQP_HOST", "localhost")
AMQP_PORT = env_var("AMQP_PORT", "5672")
AMQP_DSN = env_var("AMQP_DSN", f"amqp://{AMQP_USER}:{AMQP_PASSWORD}@{AMQP_HOST}:{AMQP_PORT}//")

# Queue from which to read Harmonia transaction messages.
TRANSACTION_QUEUE = env_var("TRANSACTION_QUEUE", "tx_matching")

# Sentry project data source name.
# https://docs.sentry.io/quickstart/#about-the-dsn
SENTRY_DSN = env_var("SENTRY_DSN")

# Environment identifier to file issues under in Sentry.
SENTRY_ENV = env_var("SENTRY_ENV", default="unset").lower()

if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENV,
        integrations=[DjangoIntegration()],
    )

# Prometheus connection details
PROMETHEUS_EXPORT_MIGRATIONS = False
PROMETHEUS_LATENCY_BUCKETS = (
    0.050,
    0.125,
    0.150,
    0.2,
    0.375,
    0.450,
    0.6,
    0.8,
    1.0,
    2.0,
    3.0,
    4.0,
    6.0,
    8.0,
    10.0,
    12.0,
    15.0,
    20.0,
    30.0,
    float("inf"),
)
PROMETHEUS_PUSH_GATEWAY = "http://localhost:9100"
PROMETHEUS_JOB = "atlas"
PUSH_PROMETHEUS_METRICS = env_var("PUSH_PROMETHEUS_METRICS", True)
LOGIN_URL = "two_factor:login"
