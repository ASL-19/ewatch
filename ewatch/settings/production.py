# -*- coding: utf-8 -*-
# Election Watch - To enable responsive governance and informed engagement with presidential elections
#
# Copyright (C) 2016  ASL19
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os


BUILD_ENV = 'production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
LOG_LEVEL = 'WARNING'

ALLOWED_HOSTS = ['yekray.com', 'www.yekray.com']

# Database
DB_USER = os.environ['DATABASE_USER']
DB_PASSWORD = os.environ['DATABASE_PASSWORD']
DB_HOST = os.environ['DATABASE_HOST']

# AWS Creds
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ewatch',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

from ewatch.settings.base import *

INSTALLED_APPS += [
    'storages',
    'compressor',
    'djangosecure',
]

MIDDLEWARE_CLASSES += [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
]

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# AWS related
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

# Static Files
#AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME

# Static Files
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'ewatch.s3_storages.StaticStorage'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATIC_ROOT = STATICFILES_LOCATION

STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)

# Media Files
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'ewatch.s3_storages.MediaStorage'
MEDIA_ROOT = MEDIAFILES_LOCATION

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_DOMAIN = '.yekray.com'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = '.yekray.com'

PAGE_CACHE = 0

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/ewatch.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },  
        'request_handler': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django_request.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'root': {
        'handlers': ['default'],
        'level': LOG_LEVEL,
    },
    'loggers': {
        'django.request': {
            'handlers': ['request_handler'],
            'level': LOG_LEVEL,
            'propagate': False
        },
    }
}
