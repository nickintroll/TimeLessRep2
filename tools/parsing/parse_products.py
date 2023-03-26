from requests_html import HTMLSession
from time import sleep

def collect_categories(file):
	cats = []
	for line in file.readlines():
		if '\t' in line:
			cats.append({
				'title': 	line.split('|')[0],
				'url':		line.split('|')[1].replace(' ', '').replace('\n', ''),
			})
	return cats



def get_products_list(category: dict, session: HTMLSession, file):
	prods = []

	category['url'] = category['url'] + '?Page=_'
	print('url:', category['url'])
	req = session.get(category['url'].replace('_', '1'))

	try:
		last_page = req.html.element('#ctl00_ctl00_b_b_ucPagerHead')[0].cssselect('a')[-1].text
	except IndexError:
		last_page = 5;
		# print('Could not find last page number, skip')
		# return 

	for page_num in range(1, int(last_page) +1):
		req = session.get(category['url'].replace('_', str(page_num)))

		if req.status_code == 404:
			break
		else:
			print('page_number: ', page_num)
	
			for i in req.html.element('.catheader'):
				print(category['title'],' | ', 'https://exist.ru/'+i.attrib['href'])
				file.write(f"{category['title']} | https://exist.ru/{i.attrib['href']} \n")
			
			if page_num == 5:
				break





if __name__ == '__main__':
	print('START')
	with open('categories.txt', 'r') as file:
		categories = collect_categories(file)

	print(f"____________________________\ntotal_categories: {len(categories)}")
	

	# session = HTMLSession()
	# with open('prods.txt', 'w+') as file:
		# for category in categories:
			# print('collecting category: ', category['title'], '(', category['url'], ')')
			# prods = get_products_list(category, session, file)
					

