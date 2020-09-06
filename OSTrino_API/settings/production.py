from os import environ
from .base import *

def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
    raise ImproperlyConfigured(error_msg)

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_setting('DB_NAME'),
        'USER': get_env_setting('DB_USER'),
        'PASSWORD': get_env_setting('DB_PASSWORD'),
        'HOST': get_env_setting('SQL_HOST'),
        'PORT': get_env_setting('SQL_PORT'),
    }
}

CORS_ORIGIN_WHITELIST = (
    get_env_setting('FRONTEND_ORIGIN'),
)
