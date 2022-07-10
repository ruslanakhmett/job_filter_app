import os


SECRET_KEY = 'refwekj4kj54kj35nr43fj34f42lf4'

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.django.db.backends.postgresql",
#         "NAME": 'django_db',
#         "USER": 'django_user',
#         "PASSWORD": '12345wW!',
#         "HOST": 'localhost',
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}