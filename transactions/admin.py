from django.contrib import admin

from .models import Wallet, Transaction, DepositType, Deposit

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
	list_display = ('owner', 'amount', 'status')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = ('wallet', 'amount', 'type', 'date', 'status')
	list_filter = ['status',]
	list_editable = ['status', ]


@admin.register(DepositType)
class DepositTypeAdmin(admin.ModelAdmin):
	list_display = ('persentage', 'minimum_deposit', )


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
	list_display = ('wallet', 'deposit_type', 'amount', 'created')
	