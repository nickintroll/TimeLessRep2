from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	# created
	path('', include('core.urls', namespace='core')),
	path('user/', include('users.urls', namespace='users')),
	path('trans/', include('transactions.urls', namespace='transaction')),

	# predefined
    path('admin/', admin.site.urls),
]

