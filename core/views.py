from django.shortcuts import render
# Create your views here.
from .models import Parameters

def get_param(name):
	try:
		return Parameters.objects.get(title=name)
	except:
		return None

def main_page(request):
	a = get_param('users_amount_main_page').value
	b = get_param('invested').value
	c = get_param('payed_off').value
		
	return render(request, 'main/main.html', {'users_amount':a, 'invested': b, 'payed_off': c})

def about_us(request):
	return render(request, 'info/about_us.html')

def partners(request):
	return render(request, 'info/partners.html')

def faq(request):
	return render(request, 'info/faq.html')

def reviews(request):
	return render(request, 'info/reviews.html')