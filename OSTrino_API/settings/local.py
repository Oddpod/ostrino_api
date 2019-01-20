from .base import *
from decouple import config

DEBUG = True
SECRET_KEY = 'jd$_5^4yy%k(k*8pyag8kt)6t$jsttugtiba*i(v#cv__i)+ys'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'USER': 'U_HELLO',
        'PASSWORD': 'hA8(scA@!fg3*sc&xaGh&6%-l<._&xCf',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'localhost',
    '127.0.0.1:8080'
)

ALLOWED_HOSTS = ['.localhost', '127.0.0.1']

os.path.join(PROJECT_ROOT, 'staticfiles')
