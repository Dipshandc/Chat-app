from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import ChatHistory
import logging

class ChatHistoryOfUser(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            # Extracting chat history pk from the URL kwargs
            chat_history_pk = view.kwargs.get('pk')  # Assuming 'pk' is the URL keyword argument

            # Ensure we have a valid ChatHistory instance
            chat_history = get_object_or_404(ChatHistory, pk=chat_history_pk)

            # Check if the user is part of the chat history's users
            if chat_history.users.filter(id=request.user.id).exists():
                return True

            # Log the denied access attempt
            logging.warning(
                f"Access denied for user {request.user} to perform action {request.method} on ChatHistory with pk {chat_history_pk}."
            )
            return False
        
        # If the user is not authenticated
        logging.warning(
            f"Access denied for unauthenticated user to perform action {request.method} on ChatHistory with pk {view.kwargs.get('pk')}."
        )
        return False
