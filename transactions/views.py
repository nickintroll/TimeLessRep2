from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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
	print(request.POST)
	print(request.GET)
	pass

def payment_form(request):
	return render('preForm.html')