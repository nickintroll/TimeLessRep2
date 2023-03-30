var res = [];
var prods = document.getElementsByClassName('prod-litems section-list')[0].getElementsByTagName('article');
for (i = 0; i<prods.length; i++) {
	console.log(i);
	let prod = prods[i];
	let price = prod.getElementsByClassName('prod-li-price');
	if (price.length != 0) {
		if (price[0].textContent != '') {
			price = price[0].textContent;
		};
	} else {
		price = '';
	};
	let about = prods[i].getElementsByClassName('page-styling prod-li-informations')[0];
	let r = {
		'title': prod.getElementsByTagName('h3')[0].textContent,
		'price': price,
		'descript' : about.getElementsByTagName('p')[0].textContent,
		'pic': prod.getElementsByTagName('img')[0]['src']
	};
	let param_names = about.getElementsByClassName('prod-li-props')[0].getElementsByTagName('dt');
	let param_values = about.getElementsByClassName('prod-li-props')[0].getElementsByTagName('dd');
	for (a=0; a < param_names.length; a++){
		r[param_names[a].textContent] = param_values[a].textContent;
	};
	res.push(r);
}
JSON.stringify(res);
