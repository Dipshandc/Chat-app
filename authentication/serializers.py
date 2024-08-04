from rest_framework import serializers
from .models import CustomUser

class UserCreateSerializer(serializers.ModelSerializer):
  id = serializers.CharField(read_only=True)
  class Meta:
    model = CustomUser
    fields = ['id','username','email','password']

  def create(self, validated_data):
    return CustomUser.objects.create_user(**validated_data)
  

class LoggedInUserDetailsSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['id','username','email']