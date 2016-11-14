from portailva.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT')
    }
}

STATIC_ROOT = "./static/"

DEBUG = os.environ.get('APP_DEBUG') == 'True'

if os.environ.get('API_DNS', False):
    ALLOWED_HOSTS.append(os.environ.get('API_DNS'))
