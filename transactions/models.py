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
	('income', 'income')
)


class Wallet(models.Model):
	owner = models.OneToOneField(Profile, related_name='wallet', on_delete=models.CASCADE)

	status = models.CharField(max_length=100, default='working', choices=wallet_status_vars)
	amount = models.FloatField(default=0)

	def is_active_wallet(self):
		if self.status == 'working':
			return True
		else:
			return False
		
	def __str__(self):
		return f"prof: {self.owner} amount:{self.amount}"

 
class Transaction(models.Model):
	wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
	amount = models.FloatField(default=0)
	
	status = models.CharField(max_length=30, default='working', choices=transaction_status_vars)
	type =models.CharField(max_length=30, default='topup', choices=transaction_types)
	
	date = models.DateTimeField(auto_now_add=True)
	

class PartnerType(models.Model):
	title = models.CharField(max_length=300)
	start_amount = models.FloatField()
	hidden = models.BooleanField(default=False)
	bonus = models.CharField(max_length=100)
