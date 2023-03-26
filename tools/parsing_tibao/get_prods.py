from catalog.models import SubCategory, Product, ProductAttribute, Photo, Category

from requests_html import HTMLSession

cats = {
	# 'AC & Electricity': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=12', 'title':'кондиционер и электричество'},
	# 'Body': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=3', 'title':'кузов'},
	# 'Brake System': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=7', 'title':'Тормозная система'},
	# 'Clutch': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=2', 'title':'сцепление'},
	# 'CrankShaft & Camshaft': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=5', 'title':'Коленчатый вал и распределительный вал'},
	# 'Driveshaft And Axle': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=19', 'title':'Приводной вал и ось'},
	# 'Electricity-Sensor': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=16', 'title':'Датчик электричества'},
	# 'Engine Air Supply': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=14', 'title':'Подача воздуха в двигатель'},
	# 'Engine Cooling': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=6', 'title':'Охлаждение двигателя'},
	# 'Engine Mountings': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=13', 'title':'Крепления двигателя'},
	# 'Ignition System': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=15', 'title':'Система зажигания'},
	# 'Lubrication System': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=10', 'title':'Система смазки'},
	# 'Modified parts': 
	# {'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=24', 'title':'Модифицированные части'},
# 
	'Engine Gasket& Head': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=4', 'title':'Прокладка двигателя и головка'},
	'Engine Timing Control': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=11', 'title':'Управление синхронизацией двигателя'},
	'Engine-Belt Drive': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=8', 'title':'Двигатель-ременной привод'},
	'entire vehicle Handle': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=22', 'title':'Все автомобильные ручки'},
	'Fuel Supply System': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=18', 'title':'Система подачи топлива'},
	'Oil Class & Antifreeze': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=23', 'title':'Класс масла и антифриз'},


	'Starter System': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=17', 'title':'Стартовая система'},
	'Steering System': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=9', 'title':'Рулевая система'},
	'Other': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=21', 'title':'Другое'},
	'Suspension': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=1', 'title':'подвеска автомобиля'},
	'Transmission': 
	{'href': 'https://www.tibao.ae/asp/asp.php?action=srchcat&category=20', 'title':'Трансмиссия'},
}


def get_last_page_number(pagination):
	num = 1
	for i in pagination:
		if i.text.isdigit():
			num = i.text
	
	return num


def collect_prods_create_cat(session, cat):
	print(cat['title'])

	prods = []
	category = Category.objects.get(slug='avtozapchasti')
	try:
		sub = SubCategory.objects.get(name=cat['title'])
	except SubCategory.DoesNotExist:
		sub = SubCategory(name=cat['title'], parent=category)
		sub.save()

	link = cat['href']
	req = session.get(link)

	last_page = get_last_page_number(req.html.find('.pagination')[0].find('li > a'))

	count = 0

	for page_num in range(int(last_page)+1):
		print(f'page: {page_num} of {last_page}')
		current = link + '&page=' + str(page_num)
		req = session.get(current)
		for prod in req.html.find('.product-slider'):

			count +=1 

			if 'OEM' in prod.text:
				title = prod.find('.tb_floatleft.tb_box > h2')[0].text
				prods.append({
					'title': title,
					'oem': prod.find('.tb_floatleft.tb_box')[0].text.split(':')[-1],
					})
				for name, val in zip(prod.find('.tb_floatleft.tb_box')[1].find('b'), prod.find('.tb_floatleft.tb_box')[1].text.split('\n')):
					prods[-1][name.text.replace('.', '')] = val.replace(name.text, '')

				try:
					prods[-1]['img'] = prod.find('img')[0].attrs['src']
				except:
					print('miss the image')
			
			print(count, '|' , prods[-1]['title'])

	return [sub, prods]


def parse():
	session = HTMLSession()

	with open('prods.text', 'a') as file:
			for cat in cats:
				try:
					cat = cats[cat]
					res = collect_prods_create_cat(session, cat)
					print(res[1], 'is done')
					file.write(f'{res[0].name}\t{str(res[1])}\n\n')
				except:
					print(cat, 'is skipped due the issue')


"""
from tools.parsing_tibao.get_prods import *
parse()
"""