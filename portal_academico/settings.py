import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url # <--- IMPORTANTE: Necesario para Vercel

# Cargar variables del archivo .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURIDAD ---
SECRET_KEY = os.getenv('SECRET_KEY', 'clave-fallbak-insegura')
DEBUG = os.getenv('DEBUG') == 'True'

# Configura los hosts permitidos
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.vercel.app']

# --- APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps de terceros
    'cloudinary_storage',
    'cloudinary',
    # Apps propias
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # WhiteNoise para estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portal_academico.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'portal_academico.wsgi.application'


# --- BASE DE DATOS ---
# 1. Configuración por defecto (Para tu PC / Local)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', 'portal_academico'),
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE_PASS', 'Cuaderno15'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': '5432',
    }
}

# 2. Configuración para Vercel (Producción)
# Verificamos si existe la variable POSTGRES_URL (Propia de Vercel) o DATABASE_URL
database_url = os.getenv('POSTGRES_URL') or os.getenv('DATABASE_URL')

if database_url:
    # Si existe la variable (estamos en Vercel), usamos esa configuración
    import dj_database_url
    db_from_env = dj_database_url.parse(database_url, conn_max_age=600, ssl_require=True)
    DATABASES['default'].update(db_from_env)


# --- VALIDACIÓN DE CONTRASEÑAS ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- IDIOMA Y ZONA HORARIA ---
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True


# --- ARCHIVOS ESTÁTICOS Y MEDIA ---

# URL pública
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Carpetas físicas
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Desarrollo
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# WhiteNoise para servir estáticos en producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirecciones Login
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# Permitir que el PDF se vea en iframes del mismo sitio
X_FRAME_OPTIONS = 'SAMEORIGIN'

# --- CONFIGURACIÓN CLOUDINARY ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    'SECURE_URL': True  # <--- CRÍTICO: Fuerza HTTPS para que no falle el visor de PDF
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'