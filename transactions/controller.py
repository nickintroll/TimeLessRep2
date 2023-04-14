import threading as tr
from time import sleep

from .models import Deposit


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

			sleep(9*60)	# sleep for 9min			


			deps = Deposit.objects.all()
			for dep in deps:
				wallet = dep.wallet
				wallet.amount = wallet.amount + (dep.amount * dep.deposit_type.persentage)
				wallet.save()


		print('WORK: stopeed %income thread')
