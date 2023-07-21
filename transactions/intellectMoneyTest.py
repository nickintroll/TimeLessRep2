import requests
import time
import hashlib
from xml.etree import cElementTree as ElemTree


token = '94eecb5274b64d8c8769011a30335e50'
secretKey = '52095be3dd2641d184219ce64e3128e1'
secretKeyForForm = 'oyivsnnwwfautqskbajx483000504278'

def get_new_form(amount=100):
	orderId = str(int(time.time()))
	amount = str(amount)
	formId = '700541'
	cardGuid = ''
	comment = 'test'
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
	return requests.post('https://api.intellectmoney.ru/p2p/GetFormUrl',
		requestData,
		headers=headers
	)

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
		
	


"""
'<?xml version="1.0" encoding="utf-8"?>\r\n<Response xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\r\n  <OperationState>\r\n    <Code>0</Code>\r\n    <Desc>Успешно обработана</Desc>\r\n  </OperationState>\r\n  <OperationId>f8b5eea8-f78a-4d48-bc1f-9686deb3d4fc</OperationId>\r\n  <FormId>700541</FormId>\r\n  <Result>\r\n    <State>\r\n      <Code>0</Code>\r\n      <Desc>Успешно обработан</Desc>\r\n    </State>\r\n    <Url>https://p2p.intellectmoney.ru/?action=getForm&amp;peerToPeerPaymentId=4578456129</Url>\r\n    <UrlBase64Encoded>aHR0cHM6Ly9wMnAuaW50ZWxsZWN0bW9uZXkucnUvP2FjdGlvbj1nZXRGb3JtJnBlZXJUb1BlZXJQYXltZW50SWQ9NDU3ODQ1NjEyOQ==</UrlBase64Encoded>\r\n  </Result>\r\n</Response>'


"""