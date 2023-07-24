from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms

from transactions.models import Transaction

from .models import SourceWallet, online_wallet_platform_all


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(
		attrs={'placeholder': 'username'}
		), label='')
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'placeholder': 'password'}
		), label='')
		

class RegisterForm(forms.ModelForm):
	password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'Passowrd'}))
	password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'Repeat passowrd'}))


	class Meta:
		model = User
		fields = ('username', 'email')
		widgets = {
			'username': forms.TextInput(attrs={'placeholder': 'Username'}),
			'email': forms.TextInput(attrs={'placeholder': 'Email'})
		}

	def clean_password(self):
		cd = self.cleaned_data
		if cd['password1'] != cd['password2']:
			raise ValidationError('Password do\'t match.')
		else:
			return cd['password2']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["username"].label = ''
		self.fields["username"].help_text = ''
		self.fields["email"].label = ''


class SourceWalletForm(forms.ModelForm):
	class Meta:
		model = SourceWallet
		fields = ('identification', )
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["identification"].label = ''


class TopUpAndWithdrawForm(forms.ModelForm):
	source = forms.ChoiceField()
	class Meta:
		model = Transaction
		fields = ('amount', 'deposit_type')
	
	def __init__(self ,*args, is_withdraw=False, **kwargs):
		super(TopUpAndWithdrawForm, self).__init__(*args, **kwargs)
		self.fields['source'].choices = sources

		if is_withdraw == True:
			del self.fields['deposit_type']
	# def is_valid(self, *args, **kwargs):
		# return super().is_valid(*args, **kwargs)


class ReinvestForm(forms.Form):
	source = forms.ChoiceField()
	amount = forms.FloatField()
	end = forms.ChoiceField()
	
	def __init__(self, *args, source, end, **kwargs):
		super(ReinvestForm, self).__init__(*args, **kwargs)
		self.fields['source'].choices = source
		self.fields['end'].choices = end