from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import ChatHistory, Message
from .serializers import MessageSerializer

class MessagePagination(PageNumberPagination):
    page_size = 20

class ChatHistoryView(APIView):
    serializer_class = MessageSerializer
    def get(self, request, pk):
        try:
            chat_history = ChatHistory.objects.get(pk=pk)
        except ChatHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(chat_history=chat_history).order_by('sent_timestamp')
        paginator = MessagePagination()
        paginated_messages = paginator.paginate_queryset(messages, request)

        serializer = MessageSerializer(paginated_messages, many=True)
        return paginator.get_paginated_response(serializer.data)
