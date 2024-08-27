from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


def generate_random_id():
  return str(uuid.uuid4())[:5]


class CustomUser(AbstractUser):
  id = models.CharField(primary_key=True,max_length=6,default=generate_random_id)
  email = models.EmailField(unique=True)
  
  def __str__(self):
    return self.username
  
class UserStatus(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='user_status')
    status = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')])
    last_seen = models.DateTimeField(null=True)

    def __str__(self):
      return f"{self.user.username}'s Status"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(null=True,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',null=True,blank=True,default='profile_pics/default.png')
    date_of_birth= models.DateField(blank=True,null=True)
  
    def __str__(self):
      return f"{self.user.username}'s Profile"
  
class Friend(models.Model):
    PENDING = 'p'
    ACCEPTED = 'a'
    REJECTED = 'r'

    STATUS_CHOICES = [
       (PENDING, 'Pending'),
       (ACCEPTED, 'Accepted'),
       (REJECTED, 'Rejected'),
       ]
    
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_friend_request')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_friend_request')
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
           