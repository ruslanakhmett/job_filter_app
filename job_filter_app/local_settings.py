import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "django_db",
        "USER": "django_user",
        "PASSWORD": "12345wW!",
        "HOST": "127.0.0.1",
        "PORT":  5432,
    }
}