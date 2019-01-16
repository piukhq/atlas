"""
Django settings for atlas project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import logging
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
DEBUG = True

ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
    'atlas',
    '.bink-dev.com',
    '.bink-staging.com',
    '.bink.com',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'transactions',
    'ubiquity_users',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env_var("ATLAS_DATABASE_NAME", "atlas"),
        'USER': env_var("ATLAS_DATABASE_USER", "postgres"),
        'PASSWORD': env_var("ATLAS_DATABASE_PASS"),
        'HOST': env_var("ATLAS_DATABASE_HOST", "localhost"),
        'PORT': env_var("ATLAS_DATABASE_PORT", "5432"),
        'CONN_MAX_AGE': None,  # unlimited persistent connections
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


AZURE_ACCOUNT_NAME = env_var('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = env_var('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = env_var('AZURE_CONTAINER')
AZURE_TRANSACTION_BASE_DIRECTORY = env_var('AZURE_TRANSACTION_BASE_DIRECTORY', 'scheme')
AZURE_CUSTOM_DOMAIN = env_var('AZURE_CUSTOM_DOMAIN')
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

ATLAS_SERVICE_API_KEY = 'F326FD4790FBE2D74418AF059FD3J'
ATLAS_SERVICE_AUTH_HEADER = 'Token {}'.format(ATLAS_SERVICE_API_KEY)
