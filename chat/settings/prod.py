from .common import *
import dj_database_url
DEBUG = False

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = []

DATABASES = {
  "default":dj_database_url.config()
}