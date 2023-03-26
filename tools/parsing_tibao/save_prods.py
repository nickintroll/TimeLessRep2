from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen

from catalog.models import *


def work_the_line(line):
	cat = line[:line.find('\t')]
	cat = SubCategory.objects.all().filter(name=cat)[0]

	prods = eval(line[line.find('\t'):])
	
	for prod in prods:
		product = Product(
			category=cat,
			title=prod['title'],
			vendor_code=prod['oem'],
			weight='-'
		)
		product.save()
		del prod['title'], prod['oem']


		img_tmp = NamedTemporaryFile(delete=True, dir='./media', suffix='.png')
		with urlopen(prod['img']) as uo:
			if uo.status == 200:
				img_tmp.write(uo.read())
				img_tmp.flush()

				img = File(img_tmp)
				img.name=img.name.split('/')[-1]

				Photo(product=product, image=img).save()
		del prod['img']


		for key in prod.keys():
			ProductAttribute(
				product=product,
				name=key,
				value=prod[key]
			).save()


with open('prods.text', 'r') as file:
	for line in file.readlines():
		work_the_line(line)
