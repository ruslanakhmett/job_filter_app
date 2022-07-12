import os
from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config("SECRET_KEY", 'Not found')

DEBUG = config("DEBUG", 0)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


DATABASES = {
    "default": {
        "ENGINE": config("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": config("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": config("POSTGRES_USER", "user"),
        "PASSWORD": config("POSTGRES_PASSWORD", "password"),
        "HOST": config("SQL_HOST", "localhost"),
        "PORT": config("SQL_PORT", "5432"),
    }
}