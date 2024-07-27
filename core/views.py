from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import ChatHistory, Message
from .serializers import MessageSerializer
from .permissions import ChatHistoryOfUser  

class MessagePagination(PageNumberPagination):
    page_size = 20


class ChatHistoryView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, ChatHistoryOfUser]

    def get(self, request, pk):
        # Handle GET request to fetch ChatHistory and its messages
        try:
            chat_history = ChatHistory.objects.get(pk=pk)
        except ChatHistory.DoesNotExist:
            return Response(
                {"detail": "Chat history not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user has permission to access this ChatHistory
        self.check_object_permissions(request, chat_history)

        messages = Message.objects.filter(chat_history=chat_history).order_by('sent_timestamp')
        paginator = MessagePagination()
        paginated_messages = paginator.paginate_queryset(messages, request)

        serializer = MessageSerializer(paginated_messages, many=True)
        return paginator.get_paginated_response(serializer.data)
