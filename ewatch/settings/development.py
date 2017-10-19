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


BUILD_ENV = 'development'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOG_LEVEL = 'DEBUG'

ALLOWED_HOSTS = []

# Database
DB_USER = os.environ['DATABASE_USER']
DB_PASSWORD = os.environ['DATABASE_PASSWORD']
DB_HOST = os.environ['DATABASE_HOST']
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
]

from ewatch.settings.base import *

# Static Files
STATIC_ROOT = os.path.join(BASE_DIR, 'STATIC/serve')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'MEDIA')
MEDIA_URL = '/media/'

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
