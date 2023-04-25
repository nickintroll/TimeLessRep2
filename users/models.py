from django.db import models
from django.conf import settings
from django.utils.text import slugify


class PartnersLevel(models.Model):
	minimum_amount = models.FloatField()
	tax_persentage = models.FloatField()
	title = models.CharField(max_length=100)


# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

	slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

	invited_by = models.ForeignKey('profile', blank=True, null=True, on_delete=models.DO_NOTHING, related_name='invited')
	partner_status = models.ForeignKey(PartnersLevel, blank=True, null=True, related_name='profiles', on_delete=models.DO_NOTHING)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.user.username)

		return super().save(*args, **kwargs)

	def __str__(self):
			return self.user.username

	def get_absolute_url(self):
		return reverse('account:profile_other', args=[self.slug])



online_wallet_platform_all = (
	('Qiwi', 'Qiwi'),
	('SberBank', 'SberBank'),

)

class SourceWallet(models.Model):
	owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='source_wallets')

	platform = models.CharField(max_length=30, choices=online_wallet_platform_all)
	identification = models.CharField(max_length=100)


class ReferalLink(models.Model):
	owner = models.OneToOneField(Profile, related_name='referal', on_delete=models.CASCADE)
	link = models.SlugField(max_length=16)
