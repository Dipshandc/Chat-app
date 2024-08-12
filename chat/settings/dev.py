from .common import *
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

DEBUG = True

SECRET_KEY = 'django-insecure-=!*^khk#!pp_g9$p7=(oi&*g)8ekk*6vw05t9%jaq$5y022e-a'

ALLOWED_HOSTS = []

DATABASES = {
  "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
    }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
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
