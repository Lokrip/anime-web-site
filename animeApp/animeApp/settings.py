"""
Django settings for animeApp project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

AUTHENTICATION_BACKENDS = [
    # Этот класс отвечает за стандартную аутентификацию в Django. Он позволяет пользователям входить в систему, используя имя пользователя (username) и пароль, сохранённые в базе данных.
    'django.contrib.auth.backends.ModelBackend',
    
    #специальные методы аутентификации `allauth`, такие как вход в систему по электронной почте Этот класс предоставляет методы аутентификации, которые расширяют функциональность стандартного бэкенда. В частности, он позволяет использовать особенности, предоставляемые библиотекой django-allauth
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', #django.contrib.sites тоесть он нужен чтобы в одном джанго приложение подерживались несколько сайтов
    
    #модификаторы
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'rest_framework',
    'debug_toolbar',
    'mptt',
    
    #Приложение
    'main',
    'home',
    'animeWatch',
    'users',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    "allauth.account.middleware.AccountMiddleware",
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,  # Чтобы не перехватывать редиректы
}

ROOT_URLCONF = 'animeApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'home.context_processors.get_category_func',
            ],
        },
    },
]

SOCIALACCOUNT_PROVIDERS = { #Создание и найстрока провайдера на катором будет использоваться авторизаций
    "github": {
        'APP': {
            'client_id': 'Ov23li6BLds1JGMp8DWc',
            'secret': 'f3eb70eb53b171f5925fe40049fd0a514af2568b',
            'key': ''
        }
    }
}

WSGI_APPLICATION = 'animeApp.wsgi.application'



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/' #перенапровляет послле авторизаций

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'main.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'slavadorohov499@gmail.com'
EMAIL_HOST_PASSWORD = 'xzwrtlsyagmmnfir'

#Хост редиса
REDIS_HOST = '127.0.0.1' # Адрес, по которому Redis будет доступен. '0.0.0.0' означает, что Redis будет доступен на всех интерфейсах.
#Порт редиса
REDIS_PORT = '6379' # Порт, на котором Redis будет слушать входящие соединения. 6379 - это стандартный порт для Redis.

#брокер URL
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
# Параметры транспорта брокера
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} # Опции для транспорта брокера, где 'visibility_timeout' указывает время (в секундах), в течение которого задача будет недоступна для повторной обработки после получения.
# URL для хранения результатов
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0' # URL для хранения результатов выполнения задач, также указывает на Redis и использует ту же базу данных.
# Разрешенные форматы контента
CELERY_ACCEPT_CONTENT = ['application/json'] # Указывает, какие форматы контента Celery может принимать. В данном случае это JSON.
# Сериализатор задач
CELERY_TASK_SERIALIZER = 'json' # Указывает, в каком формате задачи будут сериализованы (преобразованы в строку) перед отправкой в брокер. Здесь используется JSON.
# Сериализатор результатов
CELERY_RESULT_SERIALIZER = 'json'  # Указывает, в каком формате результаты выполнения задач будут сериализованы. В данном случае также используется JSON.


SITE_ID = 1 #айди первого сайта каторый будет подерживаться


try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *