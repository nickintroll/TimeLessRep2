from catalog.models import Category, SubCategory
import os


def load_categories_to_db():

	

	with open('./tools/parsing/categories.txt') as file:
		cats = file.readlines()

	main = None
	for cat in cats:
		cat.replace('\n', '')

		if '\t' in cat:
			try:
				sub = SubCategory(name=cat.replace('\t', '').split('|')[0], parent=main)
				sub.save()
				print(sub)
			except:
				print('skipped')

		else:
			try:
				main = Category(name=cat.replace('\t', '').split('|')[0])
				main.save()
				print(main)
			except:
				print('skipped')

