from django.urls import path
# from django.conf.urls.static import static
# from django.conf import settings

from . import views


app_name = 'core'
urlpatterns = [
	path('', views.main_page, name='main'),
	path('about-us', views.about_us, name='about_us'),
	path('partners', views.partners, name='partners'),
	path('faq', views.faq, name='faq'),
	path('reviews', views.reviews, name='reviews'),
]
