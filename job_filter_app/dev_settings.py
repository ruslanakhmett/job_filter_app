import os


SECRET_KEY = 'refwekj4kj54kj35nr43fj34f42lf4'

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": 'django_db',
        "USER": 'django_user',
        "PASSWORD": '12345wW!',
        "HOST": 'localhost',
    }
}