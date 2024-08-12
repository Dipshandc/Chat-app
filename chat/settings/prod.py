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
    
