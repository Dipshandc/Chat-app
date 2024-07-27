from django.urls import path
from .views import ChatHistoryView

urlpatterns = [
  path('history/<str:pk>', ChatHistoryView.as_view(),name='index')
]