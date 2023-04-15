from django.db import models
from django.core.validators import MinValueValidator

from users.models import Profile


wallet_status_vars = (
	('blocked', 'blocked'),
	('working', 'working')
)
transaction_status_vars = (
	('error','error'),
	('denied','denied'),
	('working','working'),
	('done', 'done')
)
transaction_types = (
	('topup','topup'),
	('withdraw','withdraw'),
	('working','working'),
	('income', 'income'),
	('deposit', 'deposit')
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
		return f"prof: {self.owner} amount:{self.amount}"

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

class DepositType(models.Model):
	persentage = models.FloatField()
	minimun_deposit = models.FloatField()

	def __str__(self):
		return f'{self.persentage}% каждые 9 мин, {self.persentage*320}% через 48 часов. Минимальный платеж: {self.minimun_deposit}'


class Transaction(models.Model):
	wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
	deposit_type = models.ForeignKey(DepositType, related_name='deposit_type', on_delete=models.CASCADE, null=True, blank=True)
	amount = models.FloatField(default=0)
	
	status = models.CharField(max_length=30, default='working', choices=transaction_status_vars)
	type = models.CharField(max_length=30, default='topup', choices=transaction_types)

	date = models.DateTimeField(auto_now_add=True)
	

class Deposit(models.Model):
	wallet = models.ForeignKey(Wallet, related_name='deposits', on_delete=models.CASCADE)
	deposit_type = models.ForeignKey(DepositType, related_name='deposits', on_delete=models.CASCADE)
	amount = models.FloatField(default=0)

	def __str__(self):
		return f"deposit for:{self.wallet.owner}({self.deposit_type}) amount:{self.amount}"


class PartnerType(models.Model):
	title = models.CharField(max_length=300)
	start_amount = models.FloatField()
	hidden = models.BooleanField(default=False)
	bonus = models.CharField(max_length=100)

