"""
Django settings for voting_backend project.
Production-ready configuration using environment variables.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Security ────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-t6!6y(38)!mi-*58(s2*e09cz_=@=6@09kfnfx1oa6vt=^rkub')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

# ─── Apps ─────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'voting_api',
]

MIDDLEWARE = [
    'voting_api.cors_middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # serves static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'voting_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'voting_backend.wsgi.application'

# ─── Database ─────────────────────────────────────────────────────────────────
# Railway MySQL exposes these vars — reference them in web service Variables tab:
# MYSQLHOST     = ${{MySQL.MYSQLHOST}}
# MYSQLPORT     = ${{MySQL.MYSQLPORT}}
# MYSQLUSER     = ${{MySQL.MYSQLUSER}}
# MYSQLPASSWORD = ${{MySQL.MYSQLPASSWORD}}
# MYSQLDATABASE = ${{MySQL.MYSQLDATABASE}}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     os.environ.get('MYSQLDATABASE') or os.environ.get('DB_NAME', 'voting_system'),
        'USER':     os.environ.get('MYSQLUSER')     or os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('MYSQLPASSWORD') or os.environ.get('DB_PASSWORD', 'root'),
        'HOST':     os.environ.get('MYSQLHOST')     or os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT':     os.environ.get('MYSQLPORT')     or os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# ─── CORS ─────────────────────────────────────────────────────────────────────
# Handled by voting_api.cors_middleware.CorsMiddleware (custom, no package needed)

# ─── Password validation ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── i18n ─────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# ─── Static files ─────────────────────────────────────────────────────────────
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Email ────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'muokijr@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'mumq nheg yujn izte')