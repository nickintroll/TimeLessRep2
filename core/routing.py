from django.urls import re_path
from . import consumers

websocket_patterns = [
	re_path('', consumers.ChatConsumer),
]