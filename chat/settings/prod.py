from .common import *
import dj_database_url
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

DEBUG = False

# SECRET_KEY = env('SECRET_KEY')

SECRET_KEY = '&&8%1hi6jyvsqbs9=6wet*-o5=_&yy(8wa#k86dh$3qk!qf1=t'

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
    
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('API_KEY'),
    'API_SECRET': env('API_SECRET'),
}

# Configure Django to use Cloudinary for media files
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


CLOUDINARY = {
    'secure': True,
}
