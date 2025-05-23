from django.urls import re_path

from . import consumers


# This file is alternative for urls.py for asgi 


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
