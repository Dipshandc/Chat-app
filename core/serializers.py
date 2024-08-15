from rest_framework.serializers import ModelSerializer, Serializer
from .models import ChatHistory, Message
from authentication.models import CustomUser, UserProfile, UserStatus

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio']

class UserStatusSerializer(ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ['status', 'last_seen']

class UserStatusWithUserSerializer(ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ['user','status', 'last_seen']

class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer(read_only=True,allow_null=True)
    user_status = UserStatusSerializer(read_only=True,allow_null=True)
    class Meta:
        model = CustomUser
        fields = ['id','username','email','profile','user_status']


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
              'delivered_timestamp',
              'seen_timestamp']
