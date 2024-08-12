from .common import *
import dj_database_url

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
    
