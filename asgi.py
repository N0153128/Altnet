import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hikka.settings')
django_asgi_app = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    )
    # Just HTTP for now. (We can add other protocols later.)
})