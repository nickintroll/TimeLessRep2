from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import AddProductCartForm
from catalog.models import Product, Order, OrderItem
from catalog.forms import OrderForm

@require_POST
def cart_add(request, product_id):
	cart = Cart(request)

	product = get_object_or_404(Product, id=product_id)
	form = AddProductCartForm(request.POST)

	if form.is_valid():
		cd = form.cleaned_data
		cart.add(
			quantity=cd['quantity'],
			product=product,
			override_quantity=cd['override']
		)
	return redirect('cart:cart')


@require_POST
def cart_remove(request, product_id):
	cart = Cart(request)

	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	
	return redirect('cart:cart_detail')

def cart_detail(request):
	cart = Cart(request)
	for item in cart:
		item['update_quantity_form'] = AddProductCartForm(initial={
			'quantity': item['quantity'],
			'override': True
		})
	return render(request, 'cart.html', {'cart': cart})

def create_order_form(request):
	cart = Cart(request)
	form = OrderForm()

	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			order = form.save()
			for prod in cart:
				OrderItem(
					order = order, 
					product = prod['product'], 
					quantity = int(prod['quantity'])
				).save()
			# send notification
			return redirect('cart:order', order.slug)
			
	return render(request, 'order/form.html', {'cart': cart, 'form': form})



def order_detail(request, slug):
	order = get_object_or_404(Order, slug=slug)

	return render(request, 'order/order.html', {'order': order})
	# explain to user what's gonna happen


def secret_cart_clear(request):
	cart = Cart(request)
	cart.clear()
	return redirect('catalog:catalog')