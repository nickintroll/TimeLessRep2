from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.contrib.postgres.search import SearchVector

from cart.forms import AddProductCartForm

from .models import Product, Category, SubCategory
from .forms import CatalogSearchForm

# Create your views here.
class CatalogView(ListView):
	model = Product
	template_name = 'catalog/main.html'
	paginate_by = 25
	
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
	
		context['categories'] = Category.objects.all()
		context['form'] = CatalogSearchForm()

		page = context['page_obj'].number
		context['object_list'] = Product.objects.all()[self.paginate_by*(page - 1):page*self.paginate_by]

		form = CatalogSearchForm(self.request.GET)
		if form.is_valid() and form.cleaned_data['request'] != None:
			context['form'] = form
			
			print(form.cleaned_data['request'])

			context['object_list'] = Product.objects.all().annotate(
				search = SearchVector(
					'title', 'description', 'vendor_code'
				)
			).filter(
				search=form.cleaned_data['request'],
			)
		context['total_names'] = list(Product.objects.all().values_list('title', flat=True))
		return context


class CatalogCategoryView(ListView):
	model = Product
	template_name = 'catalog/main.html'
	paginate_by = 25


	def get_context_data(self, **kwargs):
		category_slug = self.request.get_raw_uri().split('/')[-2]
		try:
			category = get_object_or_404(Category, slug=category_slug)
			is_category = True
		except:
			category = get_object_or_404(SubCategory, slug=category_slug)
			is_category = False

	
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()

		page = context['page_obj'].number
		if is_category:
			context['object_list'] = Product.objects.all().filter(category__parent=category)
		else:
			context['object_list'] = Product.objects.all().filter(category=category)

		context['form'] = CatalogSearchForm()

		form = CatalogSearchForm(self.request.GET)
		if form.is_valid() and form.cleaned_data['request'] != None:
			context['form'] = form

			context['object_list'] = context['object_list'].annotate(
				search = SearchVector(
					'title', # add here more fields to search into
				)
			)
			
			if is_category:
				context['object_list'] = context['object_list'].filter(
					search=form.cleaned_data['request'],
					category__parent=category
			)
			else:
				context['object_list'] = context['object_list'].filter(
					search=form.cleaned_data['request'],
					category=category
					)
		else:
			context['object_list'] = context['object_list'][self.paginate_by*(page - 1):page*self.paginate_by]

		# context['total_names'] = list(context['object_list'].values_list('title', flat=True))

		return context	


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
		'form': AddProductCartForm()
    }
    return render(request, 'catalog/detail.html', context)
