# Configuración para producción - Sistema de Inventario
# Usar este archivo en las instancias EC2

import os
from .settings import *

# Configuración de seguridad
DEBUG = False
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    # Agregar el DNS del ALB aquí
    'tu-alb-dns.amazonaws.com',
    # Agregar IPs de las EC2 si es necesario
]

# Configuración de base de datos PostgreSQL (RDS)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'inventory_db'),
        'USER': os.environ.get('DB_USER', 'inventory_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'inventory_password_2024'),
        'HOST': os.environ.get('DB_HOST', 'tu-rds-endpoint.amazonaws.com'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración de media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración de logging
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
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/opt/inventory-app/logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'inventory': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Configuración de caché (opcional, para mejorar rendimiento)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Configuración de sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Configuración de seguridad adicional
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuración de CORS (si es necesario)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    # Agregar dominios del ALB
]

# Configuración de timezone
TIME_ZONE = 'America/Bogota'
USE_TZ = True

# Configuración de idioma
LANGUAGE_CODE = 'es-co'
USE_I18N = True
USE_L10N = True

# Configuración específica para el experimento
INVENTORY_CONFIG = {
    'MAX_TRANSACTIONS_PER_REQUEST': 100,
    'CACHE_TIMEOUT': 300,  # 5 minutos
    'HEALTH_CHECK_TIMEOUT': 30,
    'ALB_HEALTH_CHECK_PATH': '/health-check/',
}
