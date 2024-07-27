from django.forms import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import CustomUser
from .serializers import UserCreateSerializer

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
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        return {}
