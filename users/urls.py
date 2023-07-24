from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


app_name = 'users'
urlpatterns = [
	# user
	path('login/', views.user_login, name='login'),
	path('register/', views.user_register, name='register'),
	path('prof/', views.user_profile, name='profile'),
	path('logout/', LogoutView.as_view(), name='logout'),

	# controll
	path('bonus_page/', views.bonus_page, name='bonus_page'),
	path('my_partners/', views.my_partners, name='my_partners'),
	path('withdraw/', views.withdraw, name='withdraw'),
	path('my_deposits/', views.my_deposits, name='my_deposits'),
	path('history/', views.history, name='history'),
	path('topup_wallet/', views.topup_wallet, name='topup_wallet'),
	path('promo_matireals/', views.promo_matireals, name='promo_matireals'),
	# path('settings/', views.settings, name='settings'),

	# for saving payment_wallets
	path('register/<str:ref>', views.user_register, name='register'),
	path('save_payment/<str:platform>/<str:obj_id>', views.save_platform, name='save_platform'),

]