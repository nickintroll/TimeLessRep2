from django.contrib import admin

from .models import Category, Product, Order, OrderItem, SubCategory, Photo, ProductAttribute


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {
		'slug': ('name', ),
	}

@admin.register(Product)
class ProdcutAdmin(admin.ModelAdmin):
	list_display = ['title', 'category', 'vendor_code', 'slug', 'created', 'updated', ]

	prepopulated_fields = {
		'slug': ('title', 'vendor_code'),
	}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['slug', 'contact_message']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['get_order_slug',]
	
	def get_order_slug(self, obj):
		return obj.order.slug


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
	pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	pass


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
	pass

