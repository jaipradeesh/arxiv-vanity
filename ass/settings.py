"""
For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured
import environ

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ass.papers',
    'ass.scraper',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ass.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'ass/templates')],
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

WSGI_APPLICATION = 'ass.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='psql://postgres@db:5432/postgres'),
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/'
# LOGIN_URL = '/login/'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "ass/static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "ass/static_root")

# Uploaded files, including paper source and rendered articles
MEDIA_USE_S3 = env.bool('MEDIA_USE_S3', default=False)
if MEDIA_USE_S3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
    MEDIA_URL = env('MEDIA_URL', default='https://{}.s3.amazonaws.com/'.format(
        AWS_STORAGE_BUCKET_NAME))
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = '/media/'

# Log everything to the console, including tracebacks
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# SSL
ENABLE_SSL = env.bool('ENABLE_SSL', default=False)
SESSION_COOKIE_SECURE = ENABLE_SSL
CSRF_COOKIE_SECURE = ENABLE_SSL
#SECURE_SSL_REDIRECT = ENABLE_SSL
if ENABLE_SSL:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Paper rendering
ENGRAFO_IMAGE = env('ENGRAFO_IMAGE', default='engrafo:latest')
ENGRAFO_USE_HYPER_SH = env.bool('ENGRAFO_USE_HYPER_SH', default=False)
if ENGRAFO_USE_HYPER_SH:
    if not MEDIA_USE_S3:
        raise ImproperlyConfigured('When the setting ENGRAFO_USE_HYPER_SH is True, MEDIA_USE_S3 must also be True.')
    HYPER_ACCESS_KEY = env('HYPER_ACCESS_KEY')
    HYPER_SECRET_KEY = env('HYPER_SECRET_KEY')
    HYPER_ENDPOINT = env('HYPER_ENDPOINT', default='https://us-west-1.hyper.sh:443/v1.23')
    HYPER_INSTANCE_TYPE = env('HYPER_INSTANCE_TYPE', default='s4')

# Basic auth
if env('BASICAUTH_USERNAME', default='') and env('BASICAUTH_PASSWORD'):
    BASICAUTH_USERS = {
        env('BASICAUTH_USERNAME'): env('BASICAUTH_PASSWORD')
    }
    MIDDLEWARE_CLASSES.append('basicauth.middleware.BasicAuthMiddleware')
