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


	# ['brpop_timeout', 'capacity', 'channel_capacity', 'channel_name_regex', 'client_prefix', 'close_pools', 'compile_capacities', 'connection', 'consistent_hash', 'crypter', 'decode_hosts', 'deserialize', 'expiry', 'extensions', 'flush', 'get_capacity', 'group_add', 'group_discard', 'group_expiry', 'group_name_regex', 'group_send', 'hosts', 'invalid_name_error', 'make_fernet', 'match_type_and_length', 'new_channel', 'non_local_name', 'pools', 'prefix', 'receive', 'receive_buffer', 'receive_clean_locks', 'receive_cleaners', 'receive_count', 'receive_event_loop', 'receive_lock', 'receive_single', 'ring_size', 'send', 'serialize', 'valid_channel_name', 'valid_channel_names', 'valid_group_name', 'wait_received']
	# print(dir(channel_layer))
	# print('CHANNEL LAYER GROUPS:', channel_layer.groups)
	# print('CHANNEL LAYER CHANS:', channel_layer.channels)


	# for i in dir(channel_layer):
		# print(i, ' : ', eval(f'channel_layer.{i}'))


	await channel_layer.send(channel_name, {
			'type': 'message',
			'message': message.text.split(':')[1],
			'status': '200'
		})


	await message.answer(message.from_user.username + ' ваш ответ был отправлен на '+ channel_name)


class Command(BaseCommand):
	help = 'Runs the bot for answering messages to chat'

	def handle(self, *args, **kwargs):
		print('starting rolling')
		executor.start_polling(dp)

# check

"""
"""