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
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ================================================
# 🔐 VALIDAÇÃO DE SENHA
# ================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
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

# ================================================
# 🧱 SEGURANÇA EXTRA (produção)
# ================================================
if ENVIRONMENT == "production":
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ================================================
# ⚙️ PADRÃO
# ================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"