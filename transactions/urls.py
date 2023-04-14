from django.urls import path
from .views import income_task_start, income_task_kill

app_name='transactions'
urlpatterns = [
	path('run_start_process/', income_task_start, name='start_income_thread'),
	path('stop_start_process/', income_task_kill, name='kill_income_thread'),
]