from django.urls import re_path
import common_utils.socket.consumer as consumers
from common_utils.socket.consumer import TokenDisplayConsumer

websocket_urlpatterns = [
    re_path(r'ws/send-notification/$', TokenDisplayConsumer.as_asgi()),
]