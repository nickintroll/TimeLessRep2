from django.shortcuts import render

from .models import Parameters, TextBlock


def get_texts(lang):
	texts = {}
	
	for block in TextBlock.objects.all():
		try:
			texts[block.title] = block.texts.filter(language=lang)[0].text
		except IndexError:
			print('Missing text for "', block.title, '" for ', lang)

	return texts


def render_(req, template, context={}, req_form=True):
	lang = 'ru'
	print(req.COOKIES)
	if not 'lang' in req.COOKIES:
		context['texts'] = get_texts(lang)

		req = render(req, template, context)
		req.set_cookie('lang', lang)

	else:
		context['tx'] = get_texts(req.COOKIES['lang'])

		req = render(req, template, context)

	return req


def get_param(name):
	try:
		return Parameters.objects.get(title=name)
	except:
		return None


def main_page(request):
	a = get_param('users_amount_main_page').value
	b = get_param('invested').value
	c = get_param('payed_off').value
		
	return render_(request, 'main/main.html', {'users_amount':a, 'invested': b, 'payed_off': c})


def about_us(request):
	return render_(request, 'info/about_us.html')


def partners(request):
	return render_(request, 'info/partners.html')


def faq(request):
	return render_(request, 'info/faq.html')


def reviews(request):
	return render_(request, 'info/reviews.html')
