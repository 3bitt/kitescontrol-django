import os, sys, json
from django.core.exceptions import ImproperlyConfigured
# from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# Modification to make /apps subfolder work
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


try:
    with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
        secrets = json.load(secrets_file)
except FileNotFoundError:
    raise FileNotFoundError('Configuration file is missing')

def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))


DEBUG = False
SECRET_KEY = get_secret('SECRET_KEY')

ALLOWED_HOSTS = ['batoniczny.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'dashboard',
    'instructor.instructor.apps.InstructorConfig',
    'instructor.task',
    'student',
    'lesson',
    'lesson_summary',
    'rental'
]

AUTH_USER_MODEL = 'account.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_FINDERS = [
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

ROOT_URLCONF = 'kitescontrol.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',

)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'kitescontrol.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
USE_TZ = True
TIME_ZONE = 'Europe/Warsaw'
# TIME_ZONE = 'Etc/GMT-1' - Gives error when querying with date filters
DATE_INPUT_FORMATS = ['%d-%m-%Y']
DATETIME_INPUT_FORMATS = ['%d-%m-%Y %H:%M:%S']

USE_I18N = False
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

SITE_ROOT = os.path.dirname(os.path.dirname(__file__))

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/staticfiles/'
STATICFILES_DIRS = [
    os.path.join(SITE_ROOT, 'static'),
    ]

LOGIN_URL = 'account:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'account:login'


# 3 days
CSRF_COOKIE_AGE = 259200

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASS')

if os.environ.get('DJANGO_DEVELOPMENT') is not None and os.environ.get('DJANGO_DEVELOPMENT') == 'True':
    from .settings_dev import (
        SECRET_KEY,
        DEBUG,
        ALLOWED_HOSTS,
        INSTALLED_APPS,
        TEMPLATE_LOADERS,
        LANGUAGE_CODE,
        USE_TZ,
        TIME_ZONE,
        USE_I18N,
        USE_L10N,
        SITE_ROOT,
        STATIC_ROOT,
        STATIC_URL,
        CSRF_COOKIE_SECURE,
        SESSION_COOKIE_SECURE,
        SECURE_SSL_REDIRECT,
        SECURE_HSTS_SECONDS,
        SECURE_HSTS_PRELOAD,
        SECURE_HSTS_INCLUDE_SUBDOMAINS,
        EMAIL_BACKEND,
        EMAIL_HOST,
        EMAIL_PORT,
        EMAIL_USE_TLS,
        EMAIL_HOST_USER,
        EMAIL_HOST_PASSWORD,
    )
