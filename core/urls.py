from django.urls import path
from .views import ChatHistoryView, UserListView, UserDetailsView
urlpatterns = [
  path('history/<str:name>/', ChatHistoryView.as_view(),name='chat_history_endpoint'),
  path('users/', UserListView.as_view(),name='endpoint_to_list_or_search_users '),
  path('user/<str:id>/', UserDetailsView.as_view(),name='endpoint_to_get_user_details '),
]