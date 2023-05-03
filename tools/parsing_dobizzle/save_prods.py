from django.core.files.temp import NamedTemporaryFile
from django.utils.crypto import get_random_string
from urllib.request import urlopen
from django.core.files import File
from django.db.utils import IntegrityError

from catalog.models import *


def work_on_line(line, counter):
	cat = list(SubCategory.objects.all().filter(name='Б/У'))[0]
	
	prods = line[line.find('['):]
	prods = eval(prods.replace('\n', '').replace('  ', '').replace("]'", ']'))

	for i in prods:
		counter += 1
		# product 
		print(counter, i['title'], list(i.keys()))

		if not 'Weight:' in list(i.keys()):
			i['Weight:'] = '0'

		if len(i['title']) > 99:
			title = i['title'][:96] + '...'
			i['full_title'] = i['title']
		else:
			title = i['title']

		vendor = get_random_string(8)

		prod = Product(
			category=cat,
			title= title,
			description='Без описания',
			weight= '-',
			vendor_code = vendor
		)
		prod.save()
			

		if i['img']!= '':
			img_tmp = NamedTemporaryFile(delete=True, dir='./media', suffix='.png')
			with urlopen(i['img']) as uo:
				if uo.status == 200:
					img_tmp.write(uo.read())
					img_tmp.flush()
					img = File(img_tmp)
					img.name=img.name.split('/')[-1]
					Photo(product=prod, image=img).save()
		# attrs
		leftover = i
		del leftover['title'], i['img']
		for key in leftover.keys():
			attr = ProductAttribute(
				product = prod,
				name=key,
				value=leftover[key]
			)
			attr.save()

	return counter


"""

from tools.parsing_dobizzle.save_prods import *

file = open('prods.text', 'r')
counter = 0
for line in file.readlines():
	if line.replace(' ', '').replace('\n', '') != '':
		counter = work_on_line(line, counter)

"""

# rootadminboss
# PasswordThatNooneCanHack4NoRe4sonyesididuseonethingfordifferentMea09
