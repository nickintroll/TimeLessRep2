from django.db import models
from django.conf import settings
from django.utils.text import slugify


# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

	slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.user.username)

		return super().save(*args, **kwargs)

	def __str__(self):
			return self.user.username + '.'

	def get_absolute_url(self):
		return reverse('account:profile_other', args=[self.slug])

