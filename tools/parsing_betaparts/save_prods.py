from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
from django.db.utils import IntegrityError

from catalog.models import *

def work_on_line(line, counter):	
	cat = line[:line.find('[')]
	try:
		cat = list(SubCategory.objects.all().filter(name=cat.rstrip().lstrip()))[0]
	except:
		return counter
	prods = line[line.find('['):]
	prods = eval(prods.replace('\n', '').replace('  ', '').replace("]'", ']'))
	for i in prods:
		counter += 1
		if counter < 721:
			continue	
		print(counter, i['title'], list(i.keys()))
		if not 'SKU:' in list(i.keys()):
			continue 
		if not 'Weight:' in list(i.keys()):
			i['Weight:'] = '0'
		if len(i['title']) > 99:
			title = i['title'][:96] + '...'
			i['full_title'] = i['title']
		else:
			title = i['title']
		prod = Product(
			category=cat,
			title= title,
			description=i['descript'],
			weight= float(i['Weight:'].replace(' kg', ''))*1000,
			vendor_code= i['SKU:']
		)
		try:
			prod.save()
		except IntegrityError:
			try:
				Product.objects.all().filter(vendor_code=i['SKU:'])[0].delete()
				prod.save()
			except IndexError:
				print('shit, skippting one')
		if i['pic']!= '':
			img_tmp = NamedTemporaryFile(delete=True, dir='./media', suffix='.png')
			with urlopen(i['pic']) as uo:
				if uo.status == 200:
					img_tmp.write(uo.read())
					img_tmp.flush()
					img = File(img_tmp)
					img.name=img.name.split('/')[-1]
					Photo(product=prod, image=img).save()
		# attrs
		leftover = i
		del leftover['title'], leftover['descript'], leftover['Weight:'], i['SKU:'], i['pic']
		for key in leftover.keys():
			attr = ProductAttribute(
				product = prod,
				name=key,
				value=leftover[key]
			)
			attr.save()
	return counter


"""

from tools.parsing_betaparts.save_prods import *

file = list(open('tools/parsing_betaparts/prods.text', 'r').readlines())
counter = 0
for line in file:
	if line.replace(' ', '') != '':
		counter = work_on_line(line, counter)

"""

# rootadminboss
# PasswordThatNooneCanHack4NoRe4sonyesididuseonethingfordifferentMea09
