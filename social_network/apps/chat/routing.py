from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[a-zA-Z-0-9-]+)/$', consumers.AsyncChatConsumer),
]
