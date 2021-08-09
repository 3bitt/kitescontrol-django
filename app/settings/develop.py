import os  # noqa

from settings.base import *


ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    'http://0.0.0.0',
]
CORS_ALLOW_HEADERS = ['*']
CORS_ALLOW_METHODS = ['*']

SECURE_SSL_REDIRECT = False

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

