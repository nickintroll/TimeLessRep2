from django.urls import path
from .views import income_task_start, income_task_kill, receive_payment_data

app_name='transactions'
urlpatterns = [
	path('rpr/', receive_payment_data, name='payment_data_gateway'), # https://newinvestfuture.com/trans/rpr/
	path('run_start_process/', income_task_start, name='start_income_thread'),
	path('stop_start_process/', income_task_kill, name='kill_income_thread'),
]