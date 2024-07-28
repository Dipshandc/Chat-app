from rest_framework.serializers import ModelSerializer
from .models import ChatHistory, Message
from authentication.models import CustomUser, UserProfile

class ChatHistorySerializer(ModelSerializer):
  class Meta:
    model = ChatHistory
    fields = ['name','users']

class MessageSerializer(ModelSerializer):
  class Meta:
    model = Message
    fields = ['user',
              'chat_history',
              'message',
              'media',
              'reply_of',
              'sent_timestamp',
              'deliverd_timestamp',
              'seen_timestamp']

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio']

class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email','profile']
