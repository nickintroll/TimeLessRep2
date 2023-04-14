from django.contrib import admin

from .models import SourceWallet, Profile, ReferalLink

@admin.register(SourceWallet)
class SourceWalletAdmin(admin.ModelAdmin):
	pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	pass


@admin.register(ReferalLink)
class ReferalLinkAdmin(admin.ModelAdmin):
	pass

