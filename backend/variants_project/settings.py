"""
Django settings for variants project.

This module contains all the configuration settings for the Variants
application, including database, security, logging, and third-party integrations.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================

# Django core applications
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third-party applications
THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
]

# Local applications
LOCAL_APPS = [
    'variants',
    'annotations',
    'galaxy_integration',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware configuration
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================================================================
# URL CONFIGURATION
# =============================================================================

ROOT_URLCONF = 'variants_project.urls'
WSGI_APPLICATION = 'variants_project.wsgi.application'

# =============================================================================
# TEMPLATE CONFIGURATION
# =============================================================================

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

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Flexible database configuration - SQLite for development, PostgreSQL for production
DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite3')

if DB_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'moffitt_variants'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    # Default to SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =============================================================================
# AUTHENTICATION & AUTHORIZATION
# =============================================================================

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

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC FILES CONFIGURATION
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# =============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# REST FRAMEWORK CONFIGURATION
# =============================================================================

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# =============================================================================
# CORS CONFIGURATION
# =============================================================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Only allow all origins in development

# =============================================================================
# CELERY CONFIGURATION
# =============================================================================

CELERY_ENABLED = os.getenv('CELERY_ENABLED', 'False').lower() == 'true'

if CELERY_ENABLED:
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
    CELERY_TASK_SOFT_TIME_LIMIT = 60  # 1 minute

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.getenv('LOG_FILE', 'logs/variants_project.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'variants': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': os.getenv('LOG_LEVEL', 'INFO'),
    },
}

# =============================================================================
# EXTERNAL API CONFIGURATION
# =============================================================================

# Galaxy API Configuration
GALAXY_URL = os.getenv('GALAXY_URL', '')
GALAXY_API_KEY = os.getenv('GALAXY_API_KEY', '')
GALAXY_HISTORY_ID = os.getenv('GALAXY_HISTORY_ID', '')

# Clinical Database API Configuration
CLINVAR_API_KEY = os.getenv('CLINVAR_API_KEY', '')
COSMIC_API_KEY = os.getenv('COSMIC_API_KEY', '')
CIVIC_API_URL = os.getenv('CIVIC_API_URL', 'https://civicdb.org/api')

# =============================================================================
# CACHE CONFIGURATION
# =============================================================================

# Simple in-memory cache by default (can be switched to Redis in production)
CACHE_BACKEND = os.getenv('CACHE_BACKEND', 'locmem')

if CACHE_BACKEND == 'redis':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    # Default to in-memory cache for development
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'moffitt-cache',
        }
    }

# =============================================================================
# AWS CONFIGURATION
# =============================================================================

USE_AWS = os.getenv('USE_AWS', 'False').lower() == 'true'

if USE_AWS:
    INSTALLED_APPS += ['storages']
    INSTALLED_APPS += ['django_celery_beat']
    INSTALLED_APPS += ['django_celery_results']
    
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME', 'moffitt-variants')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    S3_USE_SIGV4 = True
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_ADDRESSING_STYLE = 'virtual'
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATIC_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    SQS_QUEUE_CONFIG = {
        'ANNOTATION_QUEUE': os.getenv('AWS_SQS_ANNOTATION_QUEUE', 'moffitt-annotation-jobs'),
        'SYNC_QUEUE': os.getenv('AWS_SQS_SYNC_QUEUE', 'moffitt-sync-jobs'),
        'UPLOAD_QUEUE': os.getenv('AWS_SQS_UPLOAD_QUEUE', 'moffitt-upload-jobs'),
    }
    
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'sqs://')
    CELERY_BROKER_TRANSPORT_OPTIONS = {
        'region': AWS_REGION,
        'polling_interval': 0.1,
        'visibility_timeout': 300,
        'wait_time_seconds': 20,
    }
    CELERY_RESULT_BACKEND = 'django-db'
    CELERY_RESULT_EXTENDED = True
    CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {
        'master_name': 'mymaster'
    }
    
    RDS_DB_ENGINE = os.getenv('RDS_DB_ENGINE', 'postgresql')
    if RDS_DB_ENGINE == 'postgresql':
        DATABASES['default'].update({
            'HOST': os.getenv('RDS_DB_HOST', os.getenv('DB_HOST', 'localhost')),
            'PORT': os.getenv('RDS_DB_PORT', os.getenv('DB_PORT', '5432')),
        })
else:
    if CELERY_ENABLED:
        CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
        CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

