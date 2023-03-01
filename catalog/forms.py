from django import forms
from .models import Order

class CatalogSearchForm(forms.Form):
	request = forms.CharField()

	class Meta:
		widgets = {
			'request': forms.TextInput(attrs={'placeholder': 'search'})
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['request'].label = ''


class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('contact_message', )
		widgets = {
			'contact_message': forms.Textarea(attrs={'placeholder': 'Leave here your contact information'})
		}



	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['contact_message'].label = ''


