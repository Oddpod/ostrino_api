from .base import *
from decouple import config

STATIC_ROOT = config('STATIC')

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())