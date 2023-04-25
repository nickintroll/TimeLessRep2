from channels.layers import get_channel_layer
from django.db import models
# from .consumers import ChatConsumer


class ChatSession(models.Model):
	channel_name = models.CharField(max_length=100)


class Parameters(models.Model):
	title = models.CharField(max_length=100)
	value = models.CharField(max_length=400)
