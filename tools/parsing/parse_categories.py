from requests_html import HTMLSession
import json


def get_categories(session: HTMLSession, file):
	req = session.get('https://exist.ru/Catalog/Goods/')

	cats = req.html.element('div#ajaxupdatepanel')[0].cssselect('div.title')
	subcats = req.html.element('div#ajaxupdatepanel')[0].cssselect('div.ucatlist')
	for cat in range(len(cats)):
		cat_title = cats[cat].cssselect('a')[1].text
		cat_url = 'https://exist.ru/' + cats[cat].cssselect('a')[1].attrib['href']

		print(cat_title)
		file.write(f'{cat_title} | {cat_url}\n')

		for sub_cat in subcats[cat].cssselect('a'):
			sub_cat_title = sub_cat.text
			sub_cat_url = 'https://exist.ru/' + sub_cat.attrib['href']
			
			print('\t', sub_cat_title)
			file.write(f'\t{sub_cat_title} | {sub_cat_url} \n')

	return True


if __name__ == '__main__':
	session = HTMLSession()

	# with open('categories.txt', 'w+') as file:
		# get_categories(session, file)
