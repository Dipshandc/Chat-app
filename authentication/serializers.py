from rest_framework import serializers
from .models import CustomUser, UserProfile, UserStatus

class UserCreateSerializer(serializers.ModelSerializer):
  id = serializers.CharField(read_only=True)
  class Meta:
    model = CustomUser
    fields = ['id','username','email','password']

  def create(self, validated_data):
    return CustomUser.objects.create_user(**validated_data)
  


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio']

class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ['status', 'last_seen']

class LoggedInUserDetailsSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True,allow_null=True)
    user_status = UserStatusSerializer(read_only=True,allow_null=True)
    class Meta:
        model = CustomUser
        fields = ['id','username','email','profile','user_status']
