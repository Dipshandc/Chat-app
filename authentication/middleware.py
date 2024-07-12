from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

class TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = get_authorization_header(request).split()

        if auth_header and auth_header[0].lower() == b'bearer':
            try:
                token_key = auth_header[1].decode('utf-8')
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except (Token.DoesNotExist, UnicodeError, IndexError):
                request.user = AnonymousUser()

    def process_response(self, request, response):
        return response
