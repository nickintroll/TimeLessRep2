from django.shortcuts import render
# Create your views here.

def main_page(request):
	return render(request, 'main/main.html')

def about_us(request):
	return render(request, 'info/about_us.html')

def partners(request):
	return render(request, 'info/partners.html')

def faq(request):
	return render(request, 'info/faq.html')