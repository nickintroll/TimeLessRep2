from django.contrib import admin

from .models import SourceWallet, Profile, ReferalLink, PartnersLevel

@admin.register(SourceWallet)
class SourceWalletAdmin(admin.ModelAdmin):
	list_display = ('platform', 'identification', )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'invited_by', 'partner_status')


@admin.register(ReferalLink)
class ReferalLinkAdmin(admin.ModelAdmin):
	list_display = ('owner', 'link')


@admin.register(PartnersLevel)
class PartnersLevelAdmin(admin.ModelAdmin):
	list_display = ('minimum_amount','tax_persentage','title')
	ordering = ('minimum_amount', )