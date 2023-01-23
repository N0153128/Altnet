from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(f'ws/chat/(?P<room_id>\w+)/$', consumers.ChatConsumer.as_asgi()),

]