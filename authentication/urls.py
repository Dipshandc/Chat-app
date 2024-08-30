from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet, LoggedInUserDetailsView, FriendRequestView

urlpatterns = [
    path('register/',UserViewSet.as_view(),name='register'),
    path('loggedin_user_details/',LoggedInUserDetailsView.as_view(),name='register'),
    path('friend_request/',FriendRequestView.as_view(),name='send_friend_request'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
