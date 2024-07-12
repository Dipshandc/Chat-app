from rest_framework.serializers import ModelSerializer
from .models import ChatHistory, Message

class ChatHistorySerializer(ModelSerializer):
  class Meta:
    model = ChatHistory
    fields = ['name','users']

class MessageSerializer(ModelSerializer):
  class Meta:
    model = Message
    fields = ['user','chat_history','message','media','reply_of','sent_timestamp','deliverd_timestamp','seen_timestamp']