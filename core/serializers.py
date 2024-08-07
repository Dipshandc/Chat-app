from rest_framework.serializers import ModelSerializer
from .models import ChatHistory, Message
from authentication.models import CustomUser, UserProfile, UserStatus

class ChatHistorySerializer(ModelSerializer):
  class Meta:
    model = ChatHistory
    fields = ['name','users']

class MessageSerializer(ModelSerializer):
  class Meta:
    model = Message
    fields = ['id',
              'user',
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

class UserStatusSerializer(ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ['status', 'last_seen']

class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    user_status = UserStatusSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email','profile','user_status']

class UserProfileSerializer(ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['user','bio','profile_pic']