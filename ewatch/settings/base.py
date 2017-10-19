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


import random
import string
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
DJANGO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(DJANGO_DIR)
DB_USER = os.environ['DATABASE_USER']
DB_PASSWORD = os.environ['DATABASE_PASSWORD']
DB_HOST = os.environ['DATABASE_HOST']

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

INSTALLED_APPS = [
    'jet',
    'django.contrib.sites',
    'django.contrib.admin',
    'user_management',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'django_jalali',
    'blog',
    'wordcloud',
    'candidate',
    'timeline',
    'questionnaire',
    'preferences',
]

FIXTURE_DIRS = [
    'user_management/fixtures',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'ewatch.urls'

WSGI_APPLICATION = 'ewatch.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
}

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

# CKEditor settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_JQUERY_URL = '//code.jquery.com/jquery-latest.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'height': 200,
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Custom': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
                'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                'HiddenField']},
            '/',
            {'name': 'basicstyles',
                'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
                'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
                'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                 'Preview',
                 'Maximize',
            ]},
        ],
        'toolbar': 'Custom'
    },
}

# Django Rest Framework settings
REST_FRAMEWORK = {
    'PAGE_SIZE': 25,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': [
        'v1',
    ],
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True

try:
    SECRET_KEY
except NameError:
    SECRET_FILE = os.path.join(BASE_DIR, '.secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            SECRET_KEY = ''.join([random.SystemRandom().choice('{}{}{}'.format(string.ascii_letters, string.digits, string.punctuation)) for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters \
                to generate your secret key!' % SECRET_FILE)
