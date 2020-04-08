from .development import *

DEBUG = False

STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT')
MEDIA_ROOT = os.environ.get('DJANGO_MEDIA_ROOT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('GROUPNAME'),
        'USER': os.environ.get('GROUPNAME', 'root'),
        'PASSWORD': os.environ.get('PASSWORD', ''),
        'HOST': os.environ.get('MYSQL_HOST', 'localhost'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    }
}

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
AVATAR_STORAGE_DIR = 'avatars/'
AVATAR_CACHE_ENABLED = False
