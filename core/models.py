from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models
from uuid import uuid4

def dynamic_media_path(instance, filename):
    chat_history_slug = slugify(str(instance)) 
    return f'media/chat_history/{chat_history_slug}/{filename}'

class ChatHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    users = models.ManyToManyField(User)
     
    def get_users(self):
        return "\n".join([user.username for user in self.users.all()])

    def __str__(self):
        return f"Chat between {self.get_users()}"



class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    chat_history = models.ForeignKey(to=ChatHistory, on_delete=models.CASCADE)
    message = models.CharField(max_length=512)
    media = models.FileField(upload_to=dynamic_media_path)
    sent_timestamp = models.DateTimeField(auto_now_add=True)
    deliverd_timestamp = models.DateTimeField(blank=True,null=True)
    seen_timestamp = models.DateTimeField(blank=True,null=True)


    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
    
