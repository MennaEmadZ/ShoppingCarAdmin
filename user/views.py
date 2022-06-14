from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from .forms import RegistrationForm, BillingAddressForm, ShippingAddressForm, ProfileForm

# Create your views here.


def register_request(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		profile_form = ProfileForm(request.POST)
		billing_form = BillingAddressForm(request.POST)
		shipping_form = ShippingAddressForm(request.POST)

		if form.is_valid() and profile_form.is_valid() and billing_form.is_valid() and shipping_form.is_valid():

			user = form.save(commit=True)
			user.save()
			profile = profile_form.save(commit=False)
			billing = billing_form.save(commit=False)
			shipping = shipping_form.save(commit=False)

			username = form.cleaned_data.get('username')
			current_user = User.objects.get(username=username)

			profile.user = current_user
			billing.user = current_user
			shipping.user = current_user

			profile.save()
			billing.save()
			shipping.save()

			login(request, user)
			messages.success(request, "Registration successful.")
			return render(request, "home.html")

		messages.error(request, "Unsuccessful registration. Invalid information.")

	form = RegistrationForm()
	profile = ProfileForm()
	billing = BillingAddressForm()
	shipping = ShippingAddressForm()
	context = {"register_form": form, "profile_form": profile, "billing_form": billing, "shipping_form": shipping}

	return render(request, "registration.html", context)


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return render(request, "home.html")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form": form})


def logout_view(request):
	logout(request)
	return render(request, 'logout.html')
