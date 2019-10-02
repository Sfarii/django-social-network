"""
Django base settings for social network project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from os.path import abspath, basename, dirname, join, normpath
import sys
import environ

# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
PROJECT_NAME = basename(DJANGO_ROOT)

# collect static files here
STATIC_ROOT = join(PROJECT_ROOT, 'static')

# collect media files here
MEDIA_ROOT = join(PROJECT_ROOT, 'media')

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]

# look for translations here
PROJECT_TRANSLATIONS = [
    join(PROJECT_ROOT, 'locale'),
]

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))

# ##### ENV CONFIGURATION ############################

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env(join(PROJECT_ROOT, '.env'))

# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY
SECRET_KEY = env('SECRET_KEY', default='secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = []

# these persons receive error notification
ADMINS = (
    ('your name', 'your_name@example.com'),
)

MANAGERS = ADMINS

# ##### APPLICATION CONFIGURATION #########################

# Application definition

# the default apps
INSTALLED_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',

    # Admin panel and documentation:
    'django.contrib.admin',
    'django.contrib.admindocs',


    # Useful template tags:
    'django.contrib.humanize',

    # custom apps
    # 'apps.blog'
]

# the base middleware config
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# the base template config
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LOCALE_PATHS = PROJECT_TRANSLATIONS

LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')

TIME_ZONE = env('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ##### DJANGO RUNNING CONFIGURATION ######################

# the default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_NAME

# the root URL configuration
ROOT_URLCONF = '%s.urls' % PROJECT_NAME

# the URL for static files
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'

# the URL for media files
MEDIA_URL = '/media/'

# ##### DATABASE CONFIGURATION ############################

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# URL schema
# PostgreSQL = postgres://USER:PASSWORD@HOST:PORT/NAME
# PostGIS =	postgis://USER:PASSWORD@HOST:PORT/NAME
# MSSQL = mssql://USER:PASSWORD@HOST:PORT/NAME
# MySQL = mysql://USER:PASSWORD@HOST:PORT/NAME
# MySQL (GIS) = mysqlgis://USER:PASSWORD@HOST:PORT/NAME
# SQLite = sqlite:///PATH
# SpatiaLite = spatialite:///PATH
# Oracle = oracle://USER:PASSWORD@HOST:PORT/NAME
# Oracle (GIS) = oraclegis://USER:PASSWORD@HOST:PORT/NAME
# Redshift = redshift://USER:PASSWORD@HOST:PORT/NAME

DATABASES = {
    'default': env.db_url('DATABASE_URL', default='sqlite:///' + join(PROJECT_ROOT, 'db.sqlite3'))
}

# ##### DEBUG CONFIGURATION ###############################

DEBUG = env.bool('DEBUG', default=False)

# https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG