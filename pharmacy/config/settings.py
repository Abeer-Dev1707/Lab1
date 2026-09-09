from pathlib import Path
import os

from dotenv import load_dotenv


# ==========================================
# Base Directory
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# تحميل ملف .env
# ==========================================

load_dotenv(BASE_DIR / ".env")


# ==========================================
# Security
# ==========================================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY must be set in the .env file."
    )

DEBUG = os.getenv(
    "DEBUG",
    "True"
).lower() == "true"

ALLOWED_HOSTS = []


# ==========================================
# Django Admin Theme
# ==========================================

X_FRAME_OPTIONS = "SAMEORIGIN"

SILENCED_SYSTEM_CHECKS = [
    "security.W019"
]


# ==========================================
# Installed Apps
# ==========================================

INSTALLED_APPS = [

    # ======================================
    # Django Admin Theme
    # ======================================

    "admin_interface",
    "colorfield",

    # ======================================
    # Django Apps
    # ======================================

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # ======================================
    # Project Apps
    # ======================================

    "accounts",
    "dashboard",
    "medicines",
    "categories",
    "suppliers",
    "customers",
    "sales",
    "purchases",
    "inventory",
    "reports",
    "product_types",
    "notifications",
]


# ==========================================
# Middleware
# ==========================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==========================================
# URL Configuration
# ==========================================

ROOT_URLCONF = "config.urls"


# ==========================================
# Templates
# ==========================================

TEMPLATES = [

    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

                "notifications.context_processors.notifications_context",
            ],
        },
    },
]


# ==========================================
# WSGI
# ==========================================

WSGI_APPLICATION = "config.wsgi.application"


# ==========================================
# Database
# ==========================================

DATABASES = {

    # ======================================
    # PostgreSQL
    # ======================================

    "default": {

        "ENGINE": "django.db.backends.postgresql",

        "NAME": os.getenv(
            "DB_NAME",
            "pharmacy_db"
        ),

        "USER": os.getenv(
            "DB_USER",
            "postgres"
        ),

        "PASSWORD": os.getenv(
            "DB_PASSWORD",
            ""
        ),

        "HOST": os.getenv(
            "DB_HOST",
            "localhost"
        ),

        "PORT": os.getenv(
            "DB_PORT",
            "5432"
        ),
    },


    # ======================================
    # SQLite القديمة
    # تستخدم فقط لنقل البيانات القديمة
    # ======================================

    "old_sqlite": {

        "ENGINE": "django.db.backends.sqlite3",

        "NAME": BASE_DIR / "db.sqlite3",
    },
}


# ==========================================
# Password Validation
# ==========================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator",
    },
]


# ==========================================
# Language
# ==========================================

LANGUAGE_CODE = "ar"

TIME_ZONE = "Asia/Aden"

USE_I18N = True

USE_TZ = True


# ==========================================
# Static Files
# ==========================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ==========================================
# Media Files
# ==========================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ==========================================
# Authentication
# ==========================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "dashboard"

LOGOUT_REDIRECT_URL = "login"


# ==========================================
# Email / SMTP - Gmail
# ==========================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 465

EMAIL_USE_SSL = True

EMAIL_USE_TLS = False

EMAIL_HOST_USER = os.getenv(
    "EMAIL_HOST_USER",
    "zicoalmufti2025@gmail.com"
)

EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD",
    ""
)

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_TIMEOUT = 60


# ==========================================
# Default Auto Field
# ==========================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


# ==========================================
# Custom User Model
# ==========================================

AUTH_USER_MODEL = "accounts.User"