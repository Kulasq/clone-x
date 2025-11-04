import os
from pathlib import Path
from dotenv import load_dotenv

# ================================================
# 🔧 CONFIGURAÇÃO BASE
# ================================================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# Ambiente: "development" (local) ou "production" (servidor)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ================================================
# 🔒 SEGURANÇA - COMPATÍVEL COM PYTHONANYWHERE
# ================================================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

DEBUG = os.getenv("DEBUG", "True") == "True"
if ENVIRONMENT == "production":
    DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
if ENVIRONMENT == "production":
    ALLOWED_HOSTS.extend([
        "kulasqdev.pythonanywhere.com",
        ".pythonanywhere.com",
    ])

# ================================================
# 🔌 APLICATIVOS
# ================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "core",
    "posts",
]

# ================================================
# ⚙️ MIDDLEWARE
# ================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

if ENVIRONMENT == "production":
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ================================================
# 🧭 URLS / TEMPLATES / WSGI
# ================================================
ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "core/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ================================================
# 🧱 BANCO DE DADOS - COMPATÍVEL
# ================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ================================================
# 🔐 VALIDAÇÃO DE SENHA - MANTENDO SEGURANÇA
# ================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'users.validators.StrongPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

# ================================================
# 🌎 INTERNACIONALIZAÇÃO
# ================================================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True

# ================================================
# 🖼️ ARQUIVOS ESTÁTICOS E DE MÍDIA - COMPATÍVEL
# ================================================
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

if ENVIRONMENT == "production":
    STATIC_ROOT = "/home/kulasqdev/clone-x/staticfiles"
    MEDIA_ROOT = "/home/kulasqdev/clone-x/media"
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "core/static")]
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ================================================
# ⚙️ AUTENTICAÇÃO
# ================================================
AUTH_USER_MODEL = "users.CustomUser"
LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/users/login/"

SESSION_COOKIE_AGE = 1209600  # 2 semanas
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
if os.getenv("EMAIL_HOST"):
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@clone-x.com")

# ================================================
# 🧱 SEGURANÇA EXTRA (produção) - CORRIGINDO WARNINGS
# ================================================
SECURE_SSL_REDIRECT = ENVIRONMENT == "production"

if ENVIRONMENT == "production":
    SECURE_HSTS_SECONDS = 31536000  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

if ENVIRONMENT == "production":
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [
        "https://kulasqdev.pythonanywhere.com",
    ]

# ================================================
# 📝 LOGGING - OPICIONAL (não quebra se diretório não existir)
# ================================================
try:
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    os.makedirs(LOG_DIR, exist_ok=True)
    
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(LOG_DIR, "django.log"),
                "maxBytes": 5 * 1024 * 1024,
                "backupCount": 3,
                "formatter": "verbose",
            },
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    }
except Exception as e:
    print(f"⚠️  Logging configuration skipped: {e}")
    LOGGING = {}

# ================================================
# ⚙️ CACHE - OPICIONAL
# ================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# ================================================
# ⚙️ PADRÃO
# ================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"