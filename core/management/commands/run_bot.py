from django.core.management.base import BaseCommand

from aiogram import Bot, Dispatcher, executor
from channels.layers import get_channel_layer
from core.consumers import ChatConsumer


bot = Bot('6191435910:AAEhL8S24Gh2CWB0-W_BBD6rafoiF2Yod78')
dp = Dispatcher(bot)

@dp.message_handler()
async def get_answer(message):
	channel_layer = get_channel_layer('default')
	channel_name = message.text.split(':')[0]


	await channel_layer.send(channel_name, {
			'type': 'message',
			'message': message.text.split(':')[1],
			'status': '200'
		})


	await message.answer(message.from_user.username + '\nваш ответ был отправлен на \n'+ channel_name)


class Command(BaseCommand):
	help = 'Runs the bot for answering messages to chat'

	def handle(self, *args, **kwargs):
		print('starting rolling')
		executor.start_polling(dp)

# check

"""
"""