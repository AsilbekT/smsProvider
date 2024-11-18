import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import smsApp.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smsBackConf.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Define WebSocket protocol routing:
    "websocket": AuthMiddlewareStack(
        URLRouter(
            smsApp.routing.websocket_urlpatterns
        )
    ),
})
