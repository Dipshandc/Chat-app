import django
from .common import *
import dj_database_url
django.setup() 

DEBUG = False

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS =  env('ALLOWED_HOSTS', '').split(',')

DATABASES = {
  "default":dj_database_url.config()
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env("REDIS_URL")]
        },
    },
}

USERNAME = env('DJANGO_SUPERUSER_USERNAME')
EMAIL = env('DJANGO_SUPERUSER_EMAIL')
PASSWORD = env('DJANGO_SUPERUSER_PASSWORD')
    
if USERNAME and EMAIL and PASSWORD:
        
    if not AUTH_USER_MODEL.objects.filter(username=USERNAME).exists():
        AUTH_USER_MODEL.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print('Superuser created successfully.')
    else:
        print('Superuser already exists.')
