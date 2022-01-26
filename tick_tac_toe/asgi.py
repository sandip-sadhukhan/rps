import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tick_tac_toe.settings')
django.setup()

asgi_app = get_asgi_application()

import game.routing


application = ProtocolTypeRouter({
    'http': asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            game.routing.websocket_urlpatterns,
        ),
    ),
})
