from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Transaction
from .controller import CustomeThred
from time import sleep


secret_income_thread = None

# Create your views here.
@login_required
def income_task_start(request):
	if request.user.is_staff:
		global secret_income_thread
		if secret_income_thread == None:
			process = CustomeThred()
			process.start()
			secret_income_thread = process

	return redirect('core:main')


@login_required
def income_task_kill(request):
	if request.user.is_staff:
		global secret_income_thread
		if secret_income_thread != None:
			secret_income_thread.stop()
			secret_income_thread = None
		else: 
			print('secret_income_thread is none')
	return redirect('core:main')


def receive_payment_data(request):
	# request.POST: <QueryDict: {'orderId': ['1690471072'], 'formId': ['700541'], 'paymentId': ['4048756720'], 'amount': ['100.00'], 'date': ['2023-07-27 18:17:52'], 'comment': ['test'], 'status': ['0'], 'hash': ['9481E2C18361C52C3665A5B057B3F6BF3BF6A84F']}>
	# Transaction.objects.filter(imOrderId='1690471072')
	data = request.POST
	if not 'status' in data:
		return HttpResponse()
	else:
		if status != '0':
			# error
			return HttpResponse()
		else:
			try:
				transaction = Transaction.objects.get(imOrderId=data['orderId'][0])
			except:
				return HttpResponse()

			transaction.handle()

	return HttpResponse('data is being processed')


def payment_form(request):
	obj = Transaction.objects.latest('date')
	formUrl = 'https://p2p.intellectmoney.ru/?action=getForm&amp;peerToPeerPaymentId=4894084789'
	return render(request, 'preForm.html', {
		'formUrl': formUrl
	})
