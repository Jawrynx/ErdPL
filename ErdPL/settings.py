"""
Django settings for ErdPSL project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import dj_database_url
import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.!
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4=om+%pih5u954)#h5bni$vb92(^mx3kuan%86^dtx#yz%3b)5'

# SECURITY WARNING: don't run with debug turned on in production!!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'teams',
    'fixtures',
    'scores',
    'tournaments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ErdPL.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'ErdPL.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

AUTH_USER_MODEL = 'users.CustomUser' 

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

import os
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

GS_TYPE = os.environ.get('GS_TYPE')
GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID')
GS_PRIVATE_KEY_ID = os.environ.get('GS_PRIVATE_KEY_ID')
GS_PRIVATE_KEY = os.environ.get('GS_PRIVATE_KEY').replace('\\\\n', '\\n').encode('utf-8').decode('unicode_escape')
GS_CLIENT_EMAIL = os.environ.get('GS_CLIENT_EMAIL')
GS_CLIENT_ID = os.environ.get('GS_CLIENT_ID')
GS_AUTH_URI = os.environ.get('GS_AUTH_URI')
GS_TOKEN_URI = os.environ.get('GS_TOKEN_URI')
GS_AUTH_PROVIDER_X509_CERT_URL = os.environ.get('GS_AUTH_PROVIDER_X509_CERT_URL')
GS_CLIENT_X509_CERT_URL = os.environ.get('GS_CLIENT_X509_CERT_URL')
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')

GS_CREDENTIALS = {
    "type": GS_TYPE,
    "project_id": GS_PROJECT_ID,
    "private_key_id": GS_PRIVATE_KEY_ID,
    "private_key": GS_PRIVATE_KEY,
    "client_email": GS_CLIENT_EMAIL,
    "client_id": GS_CLIENT_ID,
    "auth_uri": GS_AUTH_URI,
    "token_uri": GS_TOKEN_URI,
    "auth_provider_x509_cert_url": GS_AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url": GS_CLIENT_X509_CERT_URL,
}

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field typee
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'