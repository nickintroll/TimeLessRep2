from django.urls import path
from .views import income_task_start, income_task_kill, receive_payment_data, payment_form

app_name='transactions'
urlpatterns = [
	path('rpr/', receive_payment_data, name='receive_payment_data'), # https://newinvestfuture.com/trans/rpr/
	path('run_start_process/', income_task_start, name='start_income_thread'),
	path('stop_start_process/', income_task_kill, name='kill_income_thread'),
	path('form_test/', payment_form, name='form_test')

]