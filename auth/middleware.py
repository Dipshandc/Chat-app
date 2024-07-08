from django.contrib.auth.models import AnonymousUser
from channels.middleware.base import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from django.conf import settings

@database_sync_to_async
def get_user(validated_token):
    try:
        user_model = get_user_model()
        user_id = jwt_decode(validated_token, settings.SECRET_KEY, algorithms=["HS256"])["user_id"]
        return user_model.objects.get(id=user_id)
    except Exception as e:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            token_name, token_key = headers[b"authorization"].decode().split()
            try:
                UntypedToken(token_key)
                scope["user"] = await get_user(token_key)
            except (InvalidToken, TokenError):
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()
        return await super().__call__(scope, receive, send)
