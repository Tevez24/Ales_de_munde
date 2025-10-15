import os
from pathlib import Path
from django.contrib.messages import constants as messages
# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Seguridad
SECRET_KEY = 'django-insecure-!q2w3e4r5t6y7u8i9o0p'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Carrito_app',
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

# URLs
ROOT_URLCONF = 'Carrito_project.urls'

# Templates
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

# WSGI
WSGI_APPLICATION = 'Carrito_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Idioma y zona horaria
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# --- Configuración de Archivos Estáticos y de Medios ---

# URL para referirse a los archivos estáticos (CSS, JavaScript, Imágenes de la plantilla)
STATIC_URL = '/static/'

# Directorios donde Django buscará archivos estáticos adicionales (fuera de las apps)
# Lo dejamos vacío por ahora ya que tus archivos están dentro de 'Carrito_app/static'
STATICFILES_DIRS = []

# Directorio donde se copiarán todos los archivos estáticos para producción (buena práctica tenerlo)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# URL para referirse a los archivos subidos por el usuario
MEDIA_URL = '/media/'

# Directorio donde se guardarán los archivos subidos por el usuario
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- Fin de la configuración ---


# Login redirect
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'inicio'

# Mensajes

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
