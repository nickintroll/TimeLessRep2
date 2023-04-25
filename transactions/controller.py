import threading as tr
from time import sleep

from .models import Deposit, Transaction
from core.models import Parameters


def get_param(name):
	try:
		return Parameters.objects.get(title = name)
	except:
		return None


class CustomeThred(tr.Thread):
	def __init__(self, *args, **kwargs):
		super(CustomeThred, self).__init__(*args, **kwargs)
		self._stop = tr.Event()

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.is_set()	

	def run(self):
		while True:
			if self.stopped():
				break

			deps = Deposit.objects.all()
			for dep in deps:
				wallet = dep.wallet
				wallet.amount = wallet.amount + (dep.amount * dep.deposit_type.persentage)
				wallet.save()

				Transaction.objects.create(amount=dep.amount * dep.deposit_type.persentage, status='done', type='income', wallet=wallet, deposit_type=dep.deposit_type)
			

			a = get_param('users_amount_main_page')
			b = get_param('invested')
			c = get_param('payed_off')

			if a != None:
				a.value = str(int(a.value) + 3)
				a.save()

			if b != None:
				b.value = str(int(b.value) + 7300)
				b.save()
			
			if c != None:			
				c.value = str(int(c.value) + 3100)
				c.save()


			sleep(9*60)	# sleep for 9min			

		print('WORK: stopeed %income thread')
