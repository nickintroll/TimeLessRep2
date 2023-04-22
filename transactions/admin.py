from django.contrib import admin

from .models import Wallet, Transaction, DepositType, Deposit

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
	list_display = ('owner', 'amount', 'status')
	pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = ('wallet', 'amount', 'date', 'type')


@admin.register(DepositType)
class DepositTypeAdmin(admin.ModelAdmin):
	pass


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
	pass
