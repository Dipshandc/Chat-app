"""
ASGI config for chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from core.routing import websocket_urlpatterns
from chat.settings.common import env

env('DJANGO_SETTINGS_MODULE')
django.setup() 
django_asgi_app = get_asgi_application()

from core.routing import websocket_urlpatterns
from authentication.middleware import JWTAuthMiddlewareStack

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
                JWTAuthMiddlewareStack(
                    URLRouter(
                        websocket_urlpatterns
                    )
                )
            )  
    }
)