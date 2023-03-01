from django import forms


class AddProductCartForm(forms.Form):
	quantity = forms.TypedChoiceField(
		choices = [(i, str(i)) for i in range(1, 71)],
		coerce = int
	)
	override = forms.BooleanField(
		required = False, 
		initial = False,
		widget = forms.HiddenInput
	)
  
	def __init__(self, *args, **kwargs):		
		super().__init__(*args, **kwargs)

		self.fields['quantity'].label = ''
