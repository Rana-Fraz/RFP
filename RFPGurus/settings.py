"""
Django settings for RFPGurus project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import datetime
import os.path
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'fbn9f506svsp@v$+ppqazpsptq38@b@+u6cn!l^t4wgne*rdsj'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

EMAIL_USE_TLS = True
EMAIL_HOST = 'bplmail.brainwade.com'
EMAIL_HOST_USER = 'no-reply@rfpgurus.com'
EMAIL_HOST_PASSWORD = '7T654Sd#eT7'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'no-reply@rfpgurus.com'

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'rfpgurus@gmail.com'
# EMAIL_HOST_PASSWORD = 'teamrfp12345'
# EMAIL_PORT = 587



# Application definition

INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'triggerr.apps.TriggerrConfig',
    'category.apps.CategoryConfig',
    'background_task',
    'simple_email_confirmation',
    'rfp.apps.RfpConfig',
    'user_functionality.apps.UserFunctionalityConfig',
    'core.apps.CoreConfig',
    'user_payment.apps.UserPaymentConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apscheduler'

]

REST_USE_JWT = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
        'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300000),
        'JWT_ALLOW_REFRESH': True,
        'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(seconds=300000),
        'JWT_AUTH_HEADER_PREFIX':'JWT'
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'core.middlewares.OneSessionPerUserMiddleware',

]
CORS_ORIGIN_ALLOW_ALL = True
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploaded_media')
MEDIA_URL = '/media/'

STATIC_URL = '/media_l/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "uploaded_media"),
    '/uploaded_media/',
]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'Content-Type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_PREFLIGHT_MAX_AGE=864000

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'localhost',
    'localhost:4200',
    'localhost:8000',
    'localhost:8080',
    '192.168.29.129:8000',
    '192.168.29.129:4200',
    '192.168.29.129:4000',
    '192.168.30.86:9000',
    '192.168.30.86:8000',
    # 'http://ns519750.ip-158-69-23.net:5010',
    'vmi228355.contaboserver.net',
    # 'http://www.coursefrenzy.com/',
    'www.rfpgurus.com/',
    'devapis.rfpgurus.com/',
    'https://devapis.rfpgurus.com/'
)

CORS_ORIGIN_WHITELIST = ('*')


ROOT_URLCONF = 'RFPGurus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'RFPGurus.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# import django css
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'