from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample, OpenApiTypes
from authentication.models import CustomUser, UserProfile
from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery
from .models import ChatHistory, Message
from .serializers import MessageSerializer, UserSerializer, UserProfileSerializer
from .permissions import ChatHistoryOfUser

class MessagePagination(PageNumberPagination):
    page_size = 20

class InitialMessagePagination(PageNumberPagination):
    page_size = 4


class ChatHistoryView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated,ChatHistoryOfUser]

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
                                    "delivered_timestamp": "2024-07-28T12:35:00Z",
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
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Chat History Not Found',
                        value={"detail": "Chat history not found."},
                        response_only=True
                    )
                ]
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
    
        chat_history =get_object_or_404(ChatHistory,name=name)
        messages = Message.objects.filter(chat_history=chat_history).order_by('-sent_timestamp')
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
                            "id": "6cc5f",
                            "username": "username",
                            "email": "useremail@gmail.com",
                            "profile": {
                            "profile_pic": "/media/profile_pics/house.jpeg",
                            "bio": "user bio"
                            },
                            "user_status": {
                            "status": "offline",
                            "last_seen": "2024-08-07T07:38:27.717376Z"
                            }
                            },
                                                        {
                            "id": "6cc5f",
                            "username": "username",
                            "email": "useremail@gmail.com",
                            "profile":"null",
                            "user_status":"null",
                            },
                        ],
                        media_type='application/json'
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Users not found",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Users Not Found',
                        value={"detail": "Users not found."},
                        response_only=True
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
            users = CustomUser.objects.select_related('profile', 'user_status').filter(username__icontains=search_term, is_superuser=False).exclude(username=current_user.username)
            if not users.exists():
                return Response(
                    {"detail": "Users not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            users = CustomUser.objects.select_related('profile', 'user_status').filter(is_superuser=False).exclude(username=current_user.username)
            if not users.exists():
                return Response(
                    {"detail": "Users not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

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
                        value=    {
                            "id": "6cc5f",
                            "username": "username",
                            "email": "useremail@gmail.com",
                            "profile": {
                            "profile_pic": "/media/profile_pics/house.jpeg",
                            "bio": "user bio"
                            },
                            "user_status": {
                            "status": "offline",
                            "last_seen": "2024-08-07T07:38:27.717376Z"
                            }
    },
                        media_type='application/json'
                    )
                ]
            ),
            404: OpenApiResponse(
                description="User not found",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'User Not Found',
                        value={"detail": "User not found."},
                        response_only=True
                    )
                ]
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


class UserProfileView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Retrieve User Profile",
        responses={
            200: UserProfileSerializer,
            404: OpenApiResponse(description="Profile not found"),
        },
        description="Fetches the profile information of the authenticated user."
    )
    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update User Profile",
        request=UserProfileSerializer,
        responses={
            200: OpenApiResponse(description="Profile updated successfully"),
            400: OpenApiResponse(description="Invalid data"),
        },
        description="Allows the authenticated user to partially update their profile information."
    )
    def patch(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": f"Profile pic of {request.user.username} edited successfully"},
                status=status.HTTP_200_OK
            )
          
class ChatHistoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Subquery to get the latest message timestamp for each chat history
        latest_message_subquery = Message.objects.filter(
            chat_history=OuterRef('pk')
        ).order_by('-sent_timestamp').values('sent_timestamp')[:1]

        # Retrieve chat histories with the latest message timestamp
        chat_histories = ChatHistory.objects.filter(users=user).annotate(
            latest_message_timestamp=Subquery(latest_message_subquery)
        ).order_by('-latest_message_timestamp')

        results = []
        for chat_history in chat_histories:
            # Get the other user in the chat
            other_user = chat_history.users.exclude(id=user.id).first()

            # Get messages for the current chat history
            messages = Message.objects.filter(chat_history=chat_history).order_by('-sent_timestamp')
            paginator = InitialMessagePagination()
            paginated_messages = paginator.paginate_queryset(messages, request)

            # Serialize messages and other user
            messages_serializer = MessageSerializer(paginated_messages, many=True)
            other_user_serializer = UserSerializer(other_user)

            # Append data to results
            results.append({
                "chat_history": chat_history.name,
                "user": other_user_serializer.data,
                "messages": messages_serializer.data
            })

        # Paginate the overall response
        paginator = MessagePagination()
        paginated_results = paginator.paginate_queryset(results, request)
        return paginator.get_paginated_response(paginated_results)