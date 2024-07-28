from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from authentication.models import CustomUser, UserProfile
from .models import ChatHistory, Message
from .serializers import MessageSerializer, UserSerializer
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


class UserListView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['username']

    def get(self, request):
        search_term = request.query_params.get('search', None)
        if search_term:
            users = CustomUser.objects.filter(username__icontains=search_term)
        else:
            users = CustomUser.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
