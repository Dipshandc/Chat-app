from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


def generate_random_id():
  return str(uuid.uuid4())[:5]


class CustomUser(AbstractUser):
  id = models.CharField(primary_key=True,max_length=6,default=generate_random_id)
  email = models.EmailField(unique=True)
  is_active = models.BooleanField(default=False)
  
  def __str__(self):
    return self.username
  