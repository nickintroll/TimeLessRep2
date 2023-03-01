from django.urls import path

from . import views

app_name='catalog'
urlpatterns = [
	path('', views.CatalogView.as_view(), name='catalog'),
	path('part/<slug:slug>/', views.product_detail, name='product_detail'),
	path('<slug:slug>/', views.CatalogCategoryView.as_view(), name='category'),
]


