from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import ChatHistory, Message

class ChatHistoryView(APIView):
  def get(self, request, pk):
    