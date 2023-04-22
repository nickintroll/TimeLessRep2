# from asgiref.sync import sync_to_async, async_to_sync 
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from channels.layers import get_channel_layer

from asyncio import run
from .answerbot import bot
from .models import ChatSession


class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = 'event'
		self.room_group_name = 'online_chat'
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		
		print('NEW CHAT CONNECTION:', self.channel_name)
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

	async def send_message_to_tg(self, bot, text, chat_id=-896489471):
		chan = get_channel_layer()

		print('SENDING MESSAGE TO TG')
		await bot.send_message(text=text, chat_id=chat_id)

	async def message(self, event, type='message'):
		print('MESSAGE TRIGGERED')
		message = event['message']
		await self.send(text_data=json.dumps({
            'message': message
		}))


	async def receive(self, text_data):

		text_json = json.loads(text_data)
		message = text_json['message']

		await self.channel_layer.send(
			self.channel_name, {
			    "type": 'message',
			    "message": message
		})


		await self.send_message_to_tg(bot, str(self.channel_name) + '\n\n' + message)
