from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-=!*^khk#!pp_g9$p7=(oi&*g)8ekk*6vw05t9%jaq$5y022e-a'

ALLOWED_HOSTS = []

DATABASES = {
  "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
    }
