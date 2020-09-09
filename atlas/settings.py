"""
Django settings for atlas project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import logging
import os

from environment import env_var, read_env

logging.basicConfig(format='%(process)s %(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('bink')
log_level = env_var("ATLAS_LOG_LEVEL", "DEBUG")
logger.setLevel(getattr(logging, log_level.upper()))

read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k@k3(kx+bdm25skdw^&d88+2(5cg@54r6$kqbjyiycsub)-g#('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_var("ATLAS_DEBUG", False)

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "127.0.0.1",
    ".bink.com",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_prometheus',
    'rest_framework',
    'prometheus_pusher.apps.PrometheusPusherConfig',
    'membership',
    'transactions',
    'ubiquity_users',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'atlas.urls'

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

WSGI_APPLICATION = 'atlas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# So apparently django_prometheus.db.backends.postgresql_psycopg2 is a db engine wrapper
# to get metrics about db queries?
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env_var("ATLAS_DATABASE_NAME", "atlas"),
        'USER': env_var("ATLAS_DATABASE_USER", "postgres"),
        'PASSWORD': env_var("ATLAS_DATABASE_PASS"),
        'HOST': env_var("ATLAS_DATABASE_HOST", "postgres"),
        'PORT': env_var("ATLAS_DATABASE_PORT", "5432"),
        'CONN_MAX_AGE': 0,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = env_var('STATIC_URL', '/static/')


AZURE_CONTAINER = env_var('AZURE_CONTAINER')
AZURE_TRANSACTION_BASE_DIRECTORY = env_var('AZURE_TRANSACTION_BASE_DIRECTORY', 'scheme')
AZURE_CUSTOM_DOMAIN = env_var('AZURE_CUSTOM_DOMAIN')
BLOB_STORAGE_DSN = env_var('BLOB_STORAGE_DSN')
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

DELETED_UBIQUITY_USERS_CONTAINER = env_var('DELETED_UBIQUITY_USERS_CONTAINER')
TRANSACTION_REPORTS_CONTAINER = env_var('TRANSACTION_REPORTS_CONTAINER')

SERVICE_API_KEY = 'F616CE5C88744DD52DB628FAD8B3D'
ATLAS_SERVICE_AUTH_HEADER = 'Token {}'.format(SERVICE_API_KEY)

<<<<<<< HEAD
# RABBITMQ DETAILS
RABBITMQ_USER = env_var('RABBITMQ_USER')
RABBITMQ_PASS = env_var('RABBITMQ_PASS')
RABBITMQ_HOST = env_var('RABBITMQ_HOST')
RABBITMQ_PORT = env_var('RABBITMQ_PORT')
CELERY_BROKER_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//'

# Transaction queue
TRANSACTION_QUEUE = env_var('TRANSACTION_QUEUE', 'tx_matching')

# Crontab
CRONTAB_HOUR = env_var('CRONTAB_HOUR', 1)
CRONTAB_MINUTES = env_var('CRONTAB_MINUTE', 0)

PROMETHEUS_LATENCY_BUCKETS = (.050, .125, .150, .2, .375, .450, .6, .8, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0, 12.0,
                              15.0, 20.0, 30.0, float("inf"))
PROMETHEUS_PUSH_GATEWAY = "http://localhost:9100"
PROMETHEUS_JOB = "atlas"
