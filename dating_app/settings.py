"""
Django settings for dating_app project.
"""
from dotenv import load_dotenv
import os
import dj_database_url

load_dotenv()

# Build paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security
SECRET_KEY = os.environ.get('secret_key')
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'profiles',
    'chat',
    'home',
    'checkout',
    'account',
    'search',
    "chatbot",  # Ứng dụng chatbot
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dating_app.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'dating_app.context_processors.engagement_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'dating_app.wsgi.application'

# Database
if "DATABASE_URL" in os.environ:
    DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Europe/London'
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True

# Ngôn ngữ và múi giờ
LANGUAGE_CODE = "vi-vn"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'profiles.backend.EmailAuth'
]

# Login/Logout settings
LOGIN_URL = '/profiles/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/preregister/'

# Message storage
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Date format
DATE_FORMAT = "d-m-Y"
DATE_INPUT_FORMATS = ['%d/%m/%Y']
USE_L10N = False


# Gemini API Key
GEMINI_API_KEY = 'AIzaSyC1qyR2i8hISRF_WTc_wfQhr4lDyORbgQ8'