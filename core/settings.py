import os
from pathlib import Path
from dotenv import load_dotenv

# ================================================
# 🔧 CONFIGURAÇÃO BASE
# ================================================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()  # Carrega variáveis do .env (apenas local)

# Ambiente: "development" (local) ou "production" (servidor)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ================================================
# 🔒 SEGURANÇA
# ================================================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "True") == "True"

if ENVIRONMENT == "production":
    DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "kulasqdev.pythonanywhere.com",
]

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

# Adiciona WhiteNoise automaticamente em produção
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
# 🧱 BANCO DE DADOS
# ================================================
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ================================================
# 🔐 VALIDAÇÃO DE SENHA
# ================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ================================================
# 🌎 INTERNACIONALIZAÇÃO
# ================================================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True

# ================================================
# 🖼️ ARQUIVOS ESTÁTICOS E DE MÍDIA
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

# Configurações de email
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@clone-x.com")

# ================================================
# 🧱 SEGURANÇA EXTRA (produção)
# ================================================
if ENVIRONMENT == "production":
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ================================================
# 📝 LOGGING
# ================================================
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
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "django.log"),
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
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# ================================================
# ⚙️ PADRÃO
# ================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
