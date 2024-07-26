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
  
class UserStatus(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')])
    last_seen = models.DateTimeField()

class UserProfile(models.Model):
   user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   bio = models.TextField(null=True,blank=True)
   profile_pic = models.ImageField(upload_to='media/profile_pics',null=True,blank=True)
   date = models.DateField(blank=True,null=True)
  
