"""
ASGI config for Ecowheels project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.routing import ProtocolTypeRouter, URLRouter
import channels.routing
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecowheels.settings')

application = get_asgi_application({
    "http": get_asgi_application(),  # Django’s ASGI app to handle traditional HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter(
            channels.routing.websocket_urlpatterns  # WebSocket URL routing
        )
    ),
})
