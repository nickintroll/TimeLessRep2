from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core import serializers

from transactions.models import Wallet, Transaction, Deposit, DepositType
from transactions.ImTools import get_new_form
from core.views import render_

from .forms import LoginForm, RegisterForm, SourceWalletForm, TopUpAndWithdrawForm, ReinvestForm
from .models import Profile, SourceWallet, online_wallet_platform_all, ReferalLink, PartnersLevel



# profile
@login_required
def bonus_page(request):
	return render_(request, 'controll/bonus.html')


@login_required
def my_partners(request):
	referal = ReferalLink.objects.filter(owner=request.user.profile)
	if len(referal) == 0:
		referal = ReferalLink.objects.create(owner=request.user.profile, link=get_random_string(16))
	else:
		referal = referal[0]

	ref_profs = Profile.objects.filter(invited_by=request.user.profile)

	return render_(request, 'controll/my_partners.html', context={'referal': referal, 'ref_profs': ref_profs})


@login_required
def my_deposits(request):
	deposits = request.user.profile.wallet.deposits.all()
	notification = None
	sources = [(i.id, i.deposit_type) for i in deposits]
	form = ReinvestForm(source=sources, end=sources)	# add source and end goal here

	if request.method == 'POST':
		form = ReinvestForm(request.POST, source=sources, end=sources)
		if form.is_valid():
			cd = form.cleaned_data

			source = deposits.filter(id=cd['source'])[0]
			if source.amount - source.deposit_type.minimum_deposit < cd['amount']:
				notification = 'На счету депозита не может оставаться сумма маньше минимального платежа'
			else:
				end = deposits.filter(id=cd['end'])[0]

				if end != source:
					end.amount = end.amount + cd['amount']
					source.amount = source.amount - cd['amount']

					source.save()
					end.save()
					notification = 'Успех! Средства переведены'
				else:
					notification = 'Вы не можете перести средства с депозита на этотже депозит'


	return render_(request, 'controll/my_deposits.html', {'deposits': deposits, 'form': form, 'notification': notification})


@login_required
def topup_wallet(request):
	pre_sources = request.user.profile.source_wallets.all()

	if len(pre_sources) == 0:
		sources = (('----', '----'), )
	else:
		sources = [(i.platform, i.platform) for i in pre_sources]

	form = TopUpAndWithdrawForm(sources=sources)
	if request.method == 'POST':
		form = TopUpAndWithdrawForm(request.POST, sources=sources)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.wallet = request.user.profile.wallet
			obj.type = 'topup'


			# no deposit
			if obj.deposit_type == None:
				notification = 'Сначала необходимо выбрать депозит'
				return render_(request, 'controll/topup_wallet.html', context={'form': TopUpAndWithdrawForm(sources=sources), 'notification': notification})

			# if amount is too low
			if obj.amount < obj.deposit_type.minimum_deposit:
				notification = f'Минимальная сумма депозита: {obj.deposit_type.minimum_deposit}р'
				return render_(request, 'controll/topup_wallet.html', context={'form': TopUpAndWithdrawForm(sources=sources), 'notification': notification})
			
			data = get_new_form(obj.amount)

			payment_form_url = data['formUrl']
			oprationId = data['data']['OperationId']
			orderId = data['orderId']
			
			obj.imOrderId = orderId
			obj.imOperationId = oprationId

			obj.save()

			return render(request, 'payment/ImForm.html', {'formUrl': payment_form_url, 'amount': amount})

			"""
			### HERE IS OLD LOGIC, WHEN PAYMENTS WERE HAPPENING INSIDE BACKEND ###
			#(basially testing logic)


			# referal tax
			ref_wal = request.user.profile.invited_by
			if ref_wal:
				if ref_wal.partner_status != None:
					pers = ref_wal.partner_status.tax_persentage
					ref_wal = ref_wal.wallet
					ref_wal.amount = ref_wal.amount + (obj.amount * pers)

					# saving transaction
					Transaction.objects.create(wallet=ref_wal, amount=obj.amount * pers, status='done', type='partner_tax')

					obj.amount = obj.amount - (obj.amount * pers)
					ref_wal.save()

			# add to deposit
			deps = Deposit.objects.all().filter(deposit_type=obj.deposit_type, wallet=obj.wallet)
			if len(deps) == 0:
				Deposit.objects.create(deposit_type=obj.deposit_type, wallet=obj.wallet, amount=obj.amount)
			else:
				deps = deps[0]
				deps.amount = deps.amount + obj.amount
				deps.save()						
			obj.save()

			# after checking with payment platform
			if obj.status == 'done':
				wal = Wallet.objects.get(id=request.user.profile.wallet.id)
				request.user.profile.wallet.amount = wal.amount + float(obj.amount)
				wal.amount = wal.amount + float(obj.amount)
				wal.save()

			notification = None
			if obj.status == 'done':
				notification = 'Успех, ваш счет был пополнен!'
				notification_class = 'notification-green'
			request.method = 'GET'

			return render_(request, 'controll/topup_wallet.html', context={'form': TopUpAndWithdrawForm(sources=sources), 'notification': notification, 'notification_class': notification_class})
			"""

	return render_(request, 'controll/topup_wallet.html', context={'form': form})


@login_required
def withdraw(request):
	sources = request.user.profile.source_wallets.all()

	if len(sources) == 0:
		sources = (('-', '-'), )
	else:
		sources = [(i.platform, i.platform) for i in sources]

	form = TopUpAndWithdrawForm(sources=sources, is_withdraw=True)
	if request.method == 'POST':
		form = TopUpAndWithdrawForm(request.POST, sources=sources, is_withdraw=True)
		if form.is_valid():
			obj = form.save(commit=False)

			if request.user.profile.wallet.amount - request.user.profile.wallet.get_deposits_summ() > obj.amount:
				obj.wallet = request.user.profile.wallet
				obj.type = 'withdraw'

				obj.status = 'done'
				# here should be some check with payment platform

				obj.save()

				if obj.status == 'done':
					wal = Wallet.objects.get(id=request.user.profile.wallet.id)
					wal.amount = wal.amount - float(obj.amount)
					wal.save()

				notification = None
				if obj.status == 'done':
					notification = 'Успех, деньги были отправлены!'
				request.method = 'GET'
				return render_(request, 'controll/withdraw.html', context={'form': TopUpAndWithdrawForm(sources=sources, is_withdraw=True), 'notification': notification})

			else:
				notification = f'Недостаточо средств на счету. доступно для вывода: {request.user.profile.wallet.amount - request.user.profile.wallet.get_deposits_summ()}p'
				return render_(request, 'controll/withdraw.html', context={'form': TopUpAndWithdrawForm(sources=sources, is_withdraw=True), 'notification': notification})

	withdraws = request.user.profile.wallet.transactions.filter(type='withdraw')

	return render_(request, 'controll/withdraw.html', context={'form': TopUpAndWithdrawForm(sources=sources, is_withdraw=True), 'wthdraws': withdraws})


@login_required
def promo_matireals(request):
	return render(request, 'controll/promo_materials.html')


@login_required
def history(request):
	trans = Transaction.objects.all().filter(wallet=request.user.profile.wallet)
	trans = serializers.serialize('json', trans)
	return render(request, 'controll/history.html', {'trans': trans})


@login_required
def settings(request):
	forms = []

	if request.method == 'POST':
		print(request.POST)

	wallets = request.user.profile.source_wallets.all()

	for platform in online_wallet_platform_all:
		platform = platform[0]
		wal = wallets.filter(platform=platform)
		if len(list(wal)) == 0:
			forms.append({
				'form':SourceWalletForm(),
				'platform': platform,
				'obj_id': None
			})
		else:
			forms.append({
				'form':SourceWalletForm(instance=wal[0]),
				'platform': platform,
				'obj_id': wal[0].id
			})

	return render(request, 'controll/setings.html', context={'forms': forms})


@login_required
def save_platform(request, platform, obj_id):
	# request.POST, platform
	form = SourceWalletForm(request.POST)
	if obj_id != 'None':
		obj = SourceWallet.objects.get(id=obj_id)
		form = SourceWalletForm(request.POST, instance=obj)
		form.save()

	if form.is_valid():
		object = form.save(commit=False)
		object.platform = platform
		object.owner = request.user.profile

		object.save()

	return redirect('users:settings')


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

	return render_(request, 'user/login.html', {'form': form, 'notification': notification})


def user_register(request, ref=None):
	form = RegisterForm()
	notification = None

	ref_profile = None
	if ref != None:
		refs = ReferalLink.objects.filter(link=ref)
		if len(refs) != 0:
			ref_profile = refs[0].owner

	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			new_user = form.save(commit=False)

			try:
				new_user.set_password(form.clean_password())

			except ValidationError:
				notification = 'Пароли не совпали'
				return render_(request, 'user/register.html', {'form': form, 'notification': notification})

			new_user.save()
			prof = Profile.objects.create(
				user = new_user,
				invited_by = ref_profile
			)
			Wallet.objects.create(
				owner = prof
			)

			login(request, new_user)
			return redirect('users:profile')
	
	if form.errors:
		errors = form.errors.as_data()
		notification = errors[list(errors.keys())[0]][0].message


	return render_(request, 'user/register.html', {'form': form, 'notification': notification})


@login_required
def user_profile(request):
	notification = ''

	user = request.user
	profile = Profile.objects.get(user=user)

	next_level = None


	if profile.partner_status == None:
		profile.partner_status = PartnersLevel.objects.filter(title='Member')[0]
		profile.save()
	

	deps_sum = profile.wallet.get_deposits_summ()
	
	for partner_lvl in PartnersLevel.objects.all():
		if partner_lvl.minimum_amount > deps_sum:
			next_level = partner_lvl
			break
		

	return render_(request, 'controll/profile.html', context={'notification': notification, 'profile':profile, 'user':user, 'next_level': next_level})
