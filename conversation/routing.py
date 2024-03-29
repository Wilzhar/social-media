# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/conversation/chat/(?P<chat_id>\w+)/$",
            consumers.ChatConsumer.as_asgi()),
]
