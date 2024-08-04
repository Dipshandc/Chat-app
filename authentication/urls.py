from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet, LoggedInUserDetailsView

urlpatterns = [
    path('register/',UserViewSet.as_view(),name='register'),
    path('loggedin_user_details/',LoggedInUserDetailsView.as_view(),name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
