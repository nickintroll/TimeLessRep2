from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


app_name = 'users'
urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('register/', views.user_register, name='register'),
	path('prof/', views.user_profile, name='profile'),
	path('logout/', LogoutView.as_view(), name='logout'),
]