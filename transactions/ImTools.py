import requests
import time
import hashlib


token = '94eecb5274b64d8c8769011a30335e50'
secretKey = '52095be3dd2641d184219ce64e3128e1'
secretKeyForForm = 'oyivsnnwwfautqskbajx483000504278'

 
def unpack_request(req):
	text = req.text
	final = {
		'req': req,
		}
	for var in text.split('<'):
		if var != '':
			var = var.split('>')
			if not '/' in var[0] and var[1].replace('\n', '').replace('\r', '').replace(' ', '') != '':
				if var[0] in final:
					final[var[0]+'In'] = var[1]
				else:
					final[var[0]] = var[1]
	return final


def get_new_form(user, deposit, amount=100):
	orderId = str(int(time.time()))
	amount = str(amount)
	formId = '700541'
	cardGuid = f'{user}:{deposit}' # those will be id's 
	comment = additional_data
	backUrl = 'https://newinvestfuture.com/user/prof/'
	language = 'ru'
	hash = ''
	signHash = ''

	# Hash
	hashArray = [orderId, amount, formId, cardGuid, comment, backUrl, language, secretKeyForForm]
	hashSignatureString = '::'.join(hashArray)
	hash = hashlib.sha1(
		bytes(hashSignatureString, 'utf-8')
		).hexdigest()
	# SignHash
	signArray = [orderId, amount, formId, cardGuid, comment, backUrl, language, secretKey]
	signString = '::'.join(signArray)
	signHash = hashlib.sha256(
		bytes(signString, 'utf-8')
	).hexdigest()

	headers = {
		'Sign': signHash,
		'Authorization': 'Bearer ' + token,
	}
	requestData = {
		'orderId': orderId,
		'amount': amount,
		'formId': formId,
		'cardGuid': cardGuid,
		'comment': comment,
		'backUrl': backUrl,
		'language': language,
		'hash': hash,
	}

	req = requests.post('https://api.intellectmoney.ru/p2p/GetFormUrl',
		requestData,
		headers=headers
	)
	data = unpack_request(req)

	return {
		'formUrl':data['Url'],
		'data': data,
		'orderId': orderId
	}	
