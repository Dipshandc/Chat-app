from .common import *
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

DEBUG = False

ALLOWED_HOSTS =  env('ALLOWED_HOSTS', '').split(',')

