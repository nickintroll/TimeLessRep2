var items = document.getElementsByClassName('sc-cmkc2d-0 dhbOk dbz-ads-listing');

res = []

for (i=0; i < items.length; i++) {
	let item = items[i];
	r = {
		'title' : item.getElementsByClassName('sc-12jmuzh-0 haTWrE heading')[0].textContent,
		'price'	: item.getElementsByClassName('sc-11jo8dj-1 cpHdIU')[0].textContent, 
		'full_name'	: item.getElementsByClassName('sc-cmkc2d-10 iOynTy')[0].textContent,
		'release_year': item.getElementsByClassName('sc-7bos3o-1 bbKsmq')[0].textContent,
		'kms': item.getElementsByClassName('sc-7bos3o-1 bbKsmq')[1].textContent,
		'color': item.getElementsByClassName('sc-7bos3o-1 bbKsmq')[3].textContent,
		'img': item.getElementsByClassName('sc-bxuil0-1 kxtgVR')[0].src
	}

	res.push(r)
}

JSON.stringify(res);
