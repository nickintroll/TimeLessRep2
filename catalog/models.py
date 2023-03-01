from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from unidecode import unidecode

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=60, db_index=True)
	slug = models.SlugField(max_length=65, unique=True)

	class Meta:
		ordering = ('name', )
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('catalog:category', args=[self.slug, ])
	
	def save(self, *args, **kwargs):
		self.slug = slugify(unidecode(self.name))
		return super().save(*args, **kwargs)
	
	def products(self):
		prods = []
		for i in self.kids.all():
			prods += i.products.all()
		return prods


class SubCategory(models.Model):
	parent = models.ForeignKey(Category, related_name='kids', on_delete=models.CASCADE)
	name = models.CharField(max_length=60, db_index=True)
	slug = models.SlugField(max_length=65, unique=True)

	class Meta:
		ordering = ('name', )
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('catalog:category', args=[self.slug, ])

	def save(self, *args, **kwargs):
		self.slug = slugify(unidecode(self.name))

		return super().save(*args, **kwargs)



class Product(models.Model):
	category = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)

	title = models.CharField(max_length=100, db_index=True)
	slug = models.SlugField(max_length=150, db_index=True, unique=True)

	vendor_code = models.CharField(max_length=100, unique=True)	
	available = models.BooleanField(default=True)
	description = models.TextField()
	weight = models.CharField(max_length=100, unique=True)
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('title', )
		index_together = (('slug', 'id'))

	def __str__(self):
		return self.title + '(' + self.vendor_code + ')'

	def get_absolute_url(self):
	    return reverse('catalog:product_detail', kwargs={'slug': self.slug})

	def save(self, *args, **kwargs):
		self.slug = slugify(unidecode(self.title))

		return super().save(*args, **kwargs)



class Photo(models.Model):
	image = models.ImageField(upload_to='prods/%Y%m%d')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class ProductAttribute(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')

	name = models.CharField(max_length=120)
	value = models.CharField(max_length=60)


class Order(models.Model):
	contact_message = models.TextField()
	slug = models.SlugField(blank=True)

	def create_slug(self):
		slug = get_random_string(24)
		others = Order.objects.filter(slug=slug)
		if len(others) != 0:
			slug = self.create_slug(self)
		else:
			return slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self.create_slug()
		super().save(*args, **kwargs)
	
	def get_total_price(self):
		return (sum([i.get_total_price() for i in self.items.all()]))

	def __iter__(self):
		for i in self.items.all():
			yield i


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	quantity = models.IntegerField()

	def get_total_price(self):
		return float(self.product.weight) * self.quantity