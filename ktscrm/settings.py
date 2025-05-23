"""
Django settings for ktscrm project.

Generated by 'django-admin startproject' using Django 3.1.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = ['http://192.168.1.19:8008',
                        'https://kateryushin.pro/',
                        'https://www.kateryushin.pro/',
                        "http://10.0.2.2:8000",
                        "https://websocketking.com",
                        "websocketking.com",
                        'kateryushin.pro',
                        ]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dogovornoy.apps.DogovornoyConfig',
    'ekc',
    'pult',
    'django.contrib.humanize',
    # 'accounts',
    'accounts.apps.AccountsConfig',
    'whitenoise.runserver_nostatic',
    'rest_framework',
    'rest_framework.authtoken',
    'panicbutton',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ktscrm.urls'

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
                'dogovornoy.context_processors.task_counter',
                'dogovornoy.context_processors.add_user_profile',
            ],
        },
    },
]

WSGI_APPLICATION = 'ktscrm.wsgi.application'


# Импорт конфиденциальных данных
try:
    from config import *
except ImportError:
    raise Exception("Не удалось найти config.py. Проверьте, что файл существует и содержит нужные настройки.")





DATABASE_ROUTERS = ['ktscrm.db_routers.EKCDbRouter', 'ktscrm.db_routers.ThirdDBRouter']


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# Переводит админку на русский
LANGUAGE_CODE = 'ru'

# Алматинское время
TIME_ZONE = 'Asia/Qyzylorda'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

#11 дериктории CSS и js
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR,'dogovornoy/static'),os.path.join(BASE_DIR, 'static'),)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

#10 дериктории для сохранения фото
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
LOGIN_URL = '/login/'
# AUTH_PROFILE_MODULE = 'profiles.Profile'

INTERNAL_IPS = [
    '*',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django_wazzup.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'panicbutton.authentication.APIKeyAuthentication',
    ],
}

INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE.insert(1, 'corsheaders.middleware.CorsMiddleware')

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "https://kateryushin.pro",
]

CORS_ALLOW_CREDENTIALS = True

ASGI_APPLICATION = "ktscrm.asgi.application"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
             "hosts": [("127.0.0.1", 6379)],  # Если Redis работает
         },
    },
}
