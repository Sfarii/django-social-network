from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from apps.chat import routing as chat_routing
from apps.blog import routing as blog_routing
from apps.account import routing as account_routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat_routing.websocket_urlpatterns + blog_routing.websocket_urlpatterns + account_routing.websocket_urlpatterns,
        )
    ),
})
