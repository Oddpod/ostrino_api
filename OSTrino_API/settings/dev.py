from OSTrino_API.settings.local import *

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')
