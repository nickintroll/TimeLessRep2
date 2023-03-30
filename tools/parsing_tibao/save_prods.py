from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
from django.db.utils import IntegrityError

from catalog.models import *


def work_the_line(line, counter):
	cat = line[:line.find('\t')]
	try:
		cat = SubCategory.objects.all().filter(name=cat)[0]
	except IndexError:
		cat = SubCategory(name=cat, parent=Category.objects.all()[0])
	print(cat)
	try:
		prods = eval(line[line.find('\t'):])
	except:
		print('could not read prods')
		return 
	
	for prod in prods:
		counter += 1
		if counter < 930:
			continue

		try:
			product = Product(
				category=cat,
				title=prod['title'],
				vendor_code=prod['oem'],
				weight='-'
			)
			product.save()
		except IntegrityError:
			print(prod['oem'], 'Is fucked')
			continue
		
		del prod['title'], prod['oem']


		img_tmp = NamedTemporaryFile(delete=True, dir='./media', suffix='.png')
		try:
			with urlopen('https://www.tibao.ae/asp/' + prod['img']) as uo:
				if uo.status == 200:
					img_tmp.write(uo.read())
					img_tmp.flush()

					img = File(img_tmp)
					img.name=img.name.split('/')[-1]

					Photo(product=product, image=img).save()
		except:
			pass
		del prod['img']


		for key in prod.keys():
			ProductAttribute(
				product=product,
				name=key,
				value=prod[key]
			).save()
		print(counter)

"""
from tools.parsing_tibao.save_prods import *

file = open('prods.text', 'r')
counter = 0
for line in file.readlines():
	if line.replace(' ', '') != '':
		counter = work_the_line(line, counter)
"""