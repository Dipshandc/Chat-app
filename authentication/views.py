from django.forms import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import CustomUser
from .serializers import UserCreateSerializer, LoggedInUserDetailsSerializer

class UserViewSet(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Create a new user",
        description="Endpoint to create a new user. Accepts user data and returns a success message.",
        request=UserCreateSerializer,
        responses={
            201: OpenApiExample(
                'User created successfully',
                value={"message": "User created successfully."},
                response_only=True,
            ),
            400: OpenApiExample(
                'Bad Request',
                value={"detail": "Invalid data."},
                response_only=True,
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        return {}

class LoggedInUserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Retrieve logged-in user details",
        description="Endpoint to retrieve the details of the currently logged-in user.",
        request=LoggedInUserDetailsSerializer,
        responses={
            200: OpenApiExample(
                'Logged-in user details',
                value={
                    "id": 1,
                    "username": "johndoe",
                    "email": "johndoe@example.com",
                },
                response_only=True,
            ),
            401: OpenApiExample(
                'Unauthorized',
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
            ),
        },
    )
    def get(self, request):
        """
        Retrieve logged-in user details.

        This endpoint allows authenticated users to retrieve their own details.
        """
        user = request.user
        serializer = LoggedInUserDetailsSerializer(user)
        return Response(serializer.data)
