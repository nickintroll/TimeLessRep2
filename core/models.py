from channels.layers import get_channel_layer
from django.db import models
# from .consumers import ChatConsumer

# Create your models here.
class ChatSession(models.Model):
	channel_name = models.CharField(max_length=100)
