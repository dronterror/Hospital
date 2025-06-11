import os
from datetime import timedelta
from pathlib import Path
import environ

# Initialize environ
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    
    # Wagtail apps
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.routable_page',
    'wagtail.contrib.settings',
    'wagtail.contrib.table_block',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'wagtail.api.v2',
    'wagtailmedia',
    'wagtail.locales',
    
    # Third-party apps
    'modelcluster',
    'taggit',
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'debug_toolbar',
    'import_export',
    'phonenumber_field',
    'ckeditor',
    'ckeditor_uploader',
    'storages',
    'guardian',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    
    # Local apps
    'hospital',
    'apps.accounts',
    'apps.appointments',
    'apps.doctors',
    'apps.patients',
    'apps.medical_records',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware',
]

ROOT_URLCONF = 'hospital_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'hospital_website.wsgi.application'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS settings
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_CREDENTIALS = True

# Database
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# Cache with Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env.str('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': env.str('REDIS_PASSWORD', default=None),
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

# Celery Configuration
CELERY_BROKER_URL = env.str('REDIS_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Debug Toolbar settings
INTERNAL_IPS = [
    '127.0.0.1',
]

# Swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Phone number field settings
PHONENUMBER_DEFAULT_REGION = 'US'
PHONENUMBER_DB_FORMAT = 'NATIONAL'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Wagtail settings
WAGTAIL_SITE_NAME = 'Hospital Website'
WAGTAILADMIN_BASE_URL = env.str('WAGTAILADMIN_BASE_URL', default='http://localhost:8000')

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
]

WAGTAILIMAGES_MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20MB
WAGTAILIMAGES_MAX_IMAGE_PIXELS = 128000000  # 128 megapixels
WAGTAILDOCS_SERVE_METHOD = 'direct'

WAGTAIL_ENABLE_UPDATE_CHECK = True
WAGTAIL_ENABLE_WHATS_NEW_BANNER = True
WAGTAIL_MODERATION_ENABLED = True

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

WAGTAIL_FRONTEND_LOGIN_URL = '/login/'
WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'registration/login.html'

# CKEditor settings for Wagtail
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

# Media settings for Wagtail
WAGTAILMEDIA_EXTENSIONS = ['mp4', 'wav', 'mp3', 'mov']
WAGTAILMEDIA_MAX_UPLOAD_SIZE = 500 * 1024 * 1024  # 500MB

# SEO settings
WAGTAIL_SEO_SITE_NAME = WAGTAIL_SITE_NAME
WAGTAIL_SEO_SITE_DESCRIPTION = 'Your trusted healthcare partner'
WAGTAIL_SEO_TWITTER_CARD = 'summary_large_image'
WAGTAIL_SEO_TWITTER_HANDLE = '@hospital'
WAGTAIL_SEO_FACEBOOK_APP_ID = ''
WAGTAIL_SEO_FACEBOOK_PUBLISHER = ''

# Cache settings for Wagtail
WAGTAIL_CACHE = True
WAGTAIL_CACHE_BACKEND = 'default'
WAGTAIL_CACHE_TIMEOUT = 60 * 15  # 15 minutes

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': env.str('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
    },
}