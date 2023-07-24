from django.db import models
from django.core.validators import MinValueValidator

from users.models import Profile
import datetime

wallet_status_vars = (
	('blocked', 'blocked'),
	('working', 'working')
)

transaction_types = (
	('topup','topup'),
	('withdraw','withdraw'),
	('working','working'),
	('income', 'income'),
	('deposit', 'deposit'),
	('partner_tax', 'partner_tax')
)


class Wallet(models.Model):
	owner = models.OneToOneField(Profile, related_name='wallet', on_delete=models.CASCADE)
	amount = models.FloatField(default=0)
	status = models.CharField(max_length=100, default='working', choices=wallet_status_vars)

	def is_active_wallet(self):
		if self.status == 'working':
			return True
		else:
			return False
		
	def __str__(self):
		return f"{self.owner}({self.amount})"

	def get_deposits_summ(self):
		res = 0
		for i in self.deposits.all():
			res += i.amount
		
		return res
	
	def get_withdraw_summ(self):
		res = 0
		
		for i in self.transactions.filter(type='withdraw'):
			res += i.amount
		
		return res

	def get_partners_summ(self):
		res = 0
		for i in self.transactions.filter(type='partner_tax'):
			res += i.amount

		return res

	def get_to_zero_but_deposit(self):
		Transaction.objects.create(wallet=self, type='groud_zero', amount=self.get_deposits_summ() - self.summ, status='done')
		self.amount = self.get_deposits_summ()
		self.save()


class DepositType(models.Model):
	persentage = models.FloatField()
	minimum_deposit = models.FloatField()

	def __str__(self):
		return f'{self.persentage}% каждые 9 мин, {self.persentage*320}% через 48 часов. Минимальный платеж: {self.minimum_deposit}'


transaction_status_vars = (
	('error','error'),
	('denied','denied'),
	('working','working'),
	('done', 'done')
)


class Transaction(models.Model):
	wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
	deposit_type = models.ForeignKey(DepositType, related_name='deposit_type', on_delete=models.CASCADE, null=True, blank=True)
	amount = models.FloatField(default=0)
	
	status = models.CharField(max_length=30, default='working', choices=transaction_status_vars)
	type = models.CharField(max_length=30, default='topup', choices=transaction_types)

	date = models.DateTimeField(auto_now_add=True)
	handle_date = models.DateTimeField(blank=True, null=True)
	imOrderId = models.TextField(blank=True, null=True)
	imOperationId = models.TextField(blank=True, null=True)
	

	def handle(self):
		# here should be changing user's wallet
		self.handle_date = datetime.datetime.now()
		self.save()


class Deposit(models.Model):
	wallet = models.ForeignKey(Wallet, related_name='deposits', on_delete=models.CASCADE)
	deposit_type = models.ForeignKey(DepositType, related_name='deposits', on_delete=models.CASCADE)
	amount = models.FloatField(default=0)

	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"deposit for:{self.wallet.owner}({self.deposit_type}) amount:{self.amount}"



"""
{
	'formUrl': 'https://p2p.intellectmoney.ru/?action=getForm&amp;peerToPeerPaymentId=4613525104', 
	'orderId': '12312312412513532'
	'data': {
		'req': <Response [200]>, 
		'Code': '0', 
		'Desc': 'Успешно обработана', 
		'OperationId': '7007acc5-8c89-4f20-907a-d6229e9e1fc4', 
		'FormId': '700541', 
		'CodeIn': '0', 
		'DescIn': 'Успешно обработан', 
		'Url': 'https://p2p.intellectmoney.ru/?action=getForm&amp;peerToPeerPaymentId=4613525104', 
		'UrlBase64Encoded': 'aHR0cHM6Ly9wMnAuaW50ZWxsZWN0bW9uZXkucnUvP2FjdGlvbj1nZXRGb3JtJnBlZXJUb1BlZXJQYXltZW50SWQ9NDYxMzUyNTEwNA=='}}
"""