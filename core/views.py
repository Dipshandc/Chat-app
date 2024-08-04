from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample, OpenApiTypes
from authentication.models import CustomUser
from django.shortcuts import get_object_or_404
from .models import ChatHistory, Message
from .serializers import MessageSerializer, UserSerializer
from .permissions import ChatHistoryOfUser

class MessagePagination(PageNumberPagination):
    page_size = 20

class ChatHistoryView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, ChatHistoryOfUser]

    @extend_schema(
        summary="Retrieve chat history messages",
        description="Endpoint to retrieve messages from a specific chat history by its name. The response is paginated.",
        request=None,
        responses={
            200: OpenApiResponse(
                description="Paginated list of messages",
                response=MessageSerializer(many=True),
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "results": [
                                {
                                    "user": 1,
                                    "chat_history": 1,
                                    "message": "Hello, how are you?",
                                    "media": None,
                                    "reply_of": None,
                                    "sent_timestamp": "2024-07-28T12:34:56Z",
                                    "deliverd_timestamp": "2024-07-28T12:35:00Z",
                                    "seen_timestamp": "2024-07-28T12:36:00Z"
                                }
                            ],
                            "count": 1,
                            "next": None,
                            "previous": None
                        },
                        media_type='application/json'
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Chat history not found",
                response=OpenApiExample(
                    'Chat History Not Found',
                    value={"detail": "Chat history not found."},
                    response_only=True
                )
            )
        },
        tags=['Chat History']
    )
    def get(self, request, name):
        """
        Retrieve chat history and its messages by ID.

        The endpoint allows authenticated users with appropriate permissions to
        retrieve a paginated list of messages for a specific chat history.
        """
        try:
            chat_history = ChatHistory.objects.get(name=name)
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

    @extend_schema(
        summary="List users with optional search",
        description="Endpoint to list all users with an optional search filter based on username.",
        parameters=[
            OpenApiParameter(name='search', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Search term to filter users by username.')
        ],
        request=None,
        responses={
            200: OpenApiResponse(
                description="List of users",
                response=UserSerializer(many=True),
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value=[
                            {
                                "id": 1,
                                "username": "johndoe",
                                "email": "johndoe@example.com",
                                "profile": [
                                    {
                                        "profile_pic": "http://example.com/profile_pic.jpg",
                                        "bio": "Software Developer"
                                    }
                                ]
                            },
                            {
                                "id": 2,
                                "username": "janedoe",
                                "email": "janedoe@example.com",
                                "profile": [
                                    {
                                        "profile_pic": "http://example.com/profile_pic2.jpg",
                                        "bio": "Graphic Designer"
                                    }
                                ]
                            }
                        ],
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=['Users']
    )
    def get(self, request):
        """
        List users with optional search by username.

        This endpoint allows authenticated users to retrieve a list of users.
        The list can be filtered by username using the `search` query parameter.
        """
        current_user = request.user
        search_term = request.query_params.get('search', None)
        if search_term:
            users = CustomUser.objects.filter(username__icontains=search_term, is_superuser=False).exclude(username=current_user.username)
        else:
            users = CustomUser.objects.filter(is_superuser=False).exclude(username=current_user.username)
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailsView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Retrieve user details",
        description="Endpoint to retrieve details of a specific user by their ID.",
        request=None,
        responses={
            200: OpenApiResponse(
                description="User details",
                response=UserSerializer,
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "id": 1,
                            "username": "johndoe",
                            "email": "johndoe@example.com",
                        },
                        media_type='application/json'
                    )
                ]
            ),
            404: OpenApiResponse(
                description="User not found",
                response=OpenApiExample(
                    'User Not Found',
                    value={"detail": "User not found."},
                    response_only=True
                )
            )
        },
        tags=['Users']
    )
    def get(self, request, id):
        """
        Retrieve user details by ID.

        This endpoint allows authenticated users to retrieve details of a specific user by their ID.
        """
        user = get_object_or_404(CustomUser, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
