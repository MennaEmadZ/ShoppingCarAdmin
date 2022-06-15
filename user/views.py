from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator  # import Paginator

from product.models import Product, ProductImage
from sale.models import Sale, SaleItem
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


def view_products(request):
	if request.method == "GET":
		products = Product.objects.all().order_by('name')

		context = {'products_list': []}

		for product in products:
			product_details = dict()
			product_details['product_info'] = product

			image = ProductImage.objects.filter(product=product.id).first()
			product_details['product_images'] = image

			context["products_list"].append(product_details)

		paginator = Paginator(context["products_list"], 24)

		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context["products_list"] = page_obj
		return render(request, "home.html", context)


def add_to_cart(request):

	if not request.user.is_authenticated:
		current_user = request.user.id
		context = {'current_user': current_user}
		return render(request, "home.html", context)

	if request.method == "POST":
		data = request.POST.get("add_cart")
		order = Sale.objects.create(user=request.user.id)
		order_item = SaleItem.objects.create(sale=order.id, product_id=data, quantity=1)

