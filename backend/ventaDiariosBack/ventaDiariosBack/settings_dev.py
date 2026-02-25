from .settings_base import *


SECRET_KEY = 'django-insecure-x#i&%g^9#c%o6w8d)o#w#6aaz6$2)6nvc=i&v18b^qve4j_lo&'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CORS permisivo para desarrollo
CORS_ALLOW_ALL_ORIGINS = True

# SQLite para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
