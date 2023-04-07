from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import LoginForm, RegisterForm
from .models import Profile


# profile
@login_required
def bonus_page(request):
	return render(request, 'controll/bonus.html')

@login_required
def my_partners(request):
	return render(request, 'controll/my_partners.html')

@login_required
def my_deposits(request):
	return render(request, 'controll/my_deposits.html')

@login_required
def topup_wallet(request):
	return render(request, 'controll/topup_wallet.html')

@login_required
def withdraw(request):
	return render(request, 'controll/withdraw.html')

@login_required
def promo_matireals(request):
	return render(request, 'controll/promo_materials.html')

@login_required
def history(request):
	return render(request, 'controll/history.html')

@login_required
def settings(request):
	return render(request, 'controll/setings.html')


# users
def user_login(request):
	form = LoginForm()
	notification = None

	if request.method == "POST":
		form = LoginForm(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(
				request, 
				username=cd['username'], 
				password=cd['password'])

			if user:

				if user.is_active:
					login(request, user)
					return redirect('users:profile')
				else:
					notification = 'Disabled account. Register new or use feed back page to contact the managers.'

			else:
				notification = 'Invalid login, try again.'
		else:
			notification = 'Wrong request, check data and try again.'

	return render(request, 'user/login.html', {'form': form, 'notification': notification})


def user_register(request):
	form = RegisterForm()
	notification = None

	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			new_user = form.save(commit=False)

			try:
				new_user.set_password(form.clean_password())

			except forms.ValidationError:
				notification = 'Passwords are don\'t match'
				return render(request, 'user/register.html', {'form': form, 'notification': notification})

			new_user.save()
			Profile.objects.create(
				user = new_user
			)
			login(request, new_user)
			return redirect('users:profile')

	return render(request, 'user/register.html', {'form': form, 'notification': notification})

@login_required
def user_profile(request):
	notification = ''

	profile = Profile.objects.get(user=request.user)
	user = request.user
	
	return render(request, 'controll/profile.html', {'notification': notification, 'profile':profile, 'user':user})
