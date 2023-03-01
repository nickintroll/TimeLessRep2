from django.urls import path
from . import views


app_name = 'cart'
urlpatterns = [
	path('', views.cart_detail, name='cart'),
	path('add/<int:product_id>', views.cart_add, name='cart_add'),
	path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),	
	path('order_create/', views.create_order_form, name='create_order'),
	path('order/<slug:slug>/', views.order_detail, name='order'),
	
	path('secret_path_to_clear_cart/', views.secret_cart_clear, name='secret_path_to_delete_cart')
]
