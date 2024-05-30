from django.db import models
from django.contrib.auth.models import User


class ChatHistory(models.Model):
    users = models.ManyToManyField(User,on_delete=models.CASCADE)

    def get_users(self):
        return "\n".join([user.username for user in self.users.all()])
    
    def __str__(self):
        return f"Chat between {self.get_users()}"

class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    ChatHistory = models.ForeignKey(to=ChatHistory, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'