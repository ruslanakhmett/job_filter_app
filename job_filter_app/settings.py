import os
from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", 0)

ALLOWED_HOSTS = config("ALLOWED_HOSTS")


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


if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'django_db_test',
           'USER': 'django_user_test',
           'PASSWORD': 'pass_test',
           'HOST': '127.0.0.1',
           'PORT': 5432,
        }
    }
    SECRET_KEY = 'test_key'
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


DJANGO_SETTINGS_MODULE="job_filter_app.settings"


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_createsuperuserwithpassword',
    'parsers_and_bot',
    'webface'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'job_filter_app.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'job_filter_app.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/staticfiles/"