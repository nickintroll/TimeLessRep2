from catalog.models import SubCategory, Product, ProductAttribute, Photo
from requests_html import HTMLSession
from django.db.models import Q
from time import sleep

from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.db.utils import IntegrityError


def load_prod_to_db(product, category):
	prod = Product()
	prod.save()
	return


def clean(line: str):
	return line.replace('\\t', '').replace('\\r', '').replace('\t', '').replace('\r', '').replace('\\n', '').replace('\n', '')


def collect_data(url, session:HTMLSession, category: SubCategory):
	prod = {}
	req = session.get(url)

	print(url)
	try:
		prod['title'] = clean(req.html.element('.fn.identifier')[0].text)
	except IndexError:
		print('no title...')
		return None
	
	try:
		prod['descript'] = clean(req.html.element('div.page-blocks.page-blocks--padding.page-content-wrapper')[1].cssselect('span')[0].text)
	except:
		prod['descript'] = ''
		print('no descript')

	prod['category'] = category
	prod['attributes'] = []
	prod['images'] = []
	prod['weight'] = ''
	prod['vendor_code'] = ''

	attr = [i for i in req.html.element('div.ZeForm.item_des')[0].getchildren() if i.tag =='div']

	for i in attr:
		name = clean(i.cssselect('div > span')[0].text)

		if 'вес' in name.lower():
			prod['weight'] = clean([a for a in i.getchildren() if a.tag =='span'][0].text)
		elif 'артикул' in name.lower():
			prod['vendor_code'] = clean([a for a in i.getchildren() if a.tag =='span'][0].text)
		else:	
			prod['attributes'].append({
				'name': name,
				'value': clean([a for a in i.getchildren() if a.tag =='span'][0].text),
			})
	
	photo = req.html.element('.photo')[0]
	if len(photo.getchildren()):
		if photo.getchildren()[0].cssselect('img')[0].attrib['src']:
			prod['images'].append(
				'http://exist.ru/' + photo.cssselect('img')[0].attrib['src']
			)

		if len(photo.getchildren()) != 1:
			for i in photo.getchildren()[1].cssselect('a'):
				prod['images'].append(
					'http://exist.ru/' + i.attrib['href']
				)
	

	return prod

def main():
	session = HTMLSession()
	with open('./tools/parsing/prods.txt', 'r') as file:
		prods = file.readlines()
	c = 0
	for prod in prods:
		c += 1
		print('prod#', c)

		category = SubCategory.objects.all().filter(Q(name__contains=clean(prod.split('|')[0]).strip()))[0]
		prod = collect_data(clean(prod.split('|')[1]).replace(' ', '').replace('exist.ru/', 'exist.ru'), session, category)

		if not prod is None:
			product = Product(
				title = prod['title'], 
				category = prod['category'], 
				weight = prod['weight'], 
				vendor_code=prod['vendor_code'], 
				description=prod['descript'],
				available=True,
			)
			try:
				product.save()
			except IntegrityError:
				print('already did this')
				continue

			for at in prod['attributes']:
				ProductAttribute(
					product = product,
					name = at['name'],
					value = at['value'][:58]
				).save()
			
			for img in prod['images']:
				img_tmp = NamedTemporaryFile(delete=True, dir='./media', suffix='.png')

				with urlopen(img) as uo:
					if uo.status == 200:
						img_tmp.write(uo.read())
						img_tmp.flush()
						
						img = File(img_tmp)
						img.name='/'.join(img.name.split('/')[-1])
						
						Photo(product=product, image=img).save()


"""
from tools.parsing import save_prods
save_prods.main()
"""	
