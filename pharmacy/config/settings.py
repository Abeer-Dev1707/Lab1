from pathlib import Path

# ==========================================
# Base Directory
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# Security
# ==========================================
SECRET_KEY = 'django-insecure-8*xmze7$@i+0og!w5ix_he8$m-v8k+oaf)wcsviu-1z)&-(#8='

DEBUG = True

ALLOWED_HOSTS = []

# ==========================================
# Installed Apps
# ==========================================
INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project Apps
    'accounts',
    'dashboard',
    'medicines',
    'categories',
    'suppliers',
    'customers',
    'sales',
    'purchases',
    'inventory',
    'reports',
    'product_types',
]

# ==========================================
# Middleware
# ==========================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==========================================
# URL Configuration
# ==========================================
ROOT_URLCONF = 'config.urls'

# ==========================================
# Templates
# ==========================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==========================================
# WSGI
# ==========================================
WSGI_APPLICATION = 'config.wsgi.application'

# ==========================================
# Database
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==========================================
# Password Validation
# ==========================================
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

# ==========================================
# Language
# ==========================================
LANGUAGE_CODE = 'ar'

TIME_ZONE = 'Asia/Aden'

USE_I18N = True

USE_TZ = True

# ==========================================
# Static Files
# ==========================================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# ==========================================
# Media Files
# ==========================================
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# ==========================================
# Authentication
# ==========================================
LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'dashboard'

LOGOUT_REDIRECT_URL = 'login'

# ==========================================
# Default Auto Field
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


