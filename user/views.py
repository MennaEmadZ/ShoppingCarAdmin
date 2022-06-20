from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator  # import Paginator

from product.forms import Quantity
from product.views import stock_count, cart_helper
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
			return redirect(view_products)

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

				cart = Sale.objects.filter(user_id=user.id, checkout=False).first()
				if not cart:
					request.session["item_total"] = 0
				else:
					total_items = SaleItem.objects.filter(sale=cart).aggregate(Sum('quantity'))
					request.session["item_total"] = total_items["quantity__sum"]

				return redirect(view_products)

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
	context = {'products_list': [], 'current_user': ''}
	products = Product.objects.all().order_by('name')

	for product in products:
		product_details = dict()
		# product info
		product_details['product_info'] = product
		# product image
		image = ProductImage.objects.filter(product=product.id).first()
		product_details['product_images'] = image
		# stock count
		product_details["stock_count"] = stock_count(product.id)

		context["products_list"].append(product_details)

	paginator = Paginator(context["products_list"], 24)

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context["products_list"] = page_obj

	# if logged in view 'add to cart' button
	if request.user.is_authenticated:
		session_user = request.user.id
		context['session_user'] = session_user

	return render(request, "home.html", context)


def add_to_cart(request, product):
	cart_helper(user=request.user.id, product=product, quantity=1)
	messages.info(request, f"Item added to the cart.")
	request.session["item_total"] += 1

	return redirect(view_products)


def cart_view(request):
	context = {'product': []}
	i = 0
	session_user = request.user.id
	cart = Sale.objects.get(user_id=session_user, checkout=False)
	cart_items = SaleItem.objects.filter(sale=cart)

	for item in cart_items:
		product_details = dict()
		product = Product.objects.get(id=item.product_id)
		product_image = ProductImage.objects.filter(product=item.product_id).first()
		i += 1
		product_details['no'] = i
		product_details['id'] = product.id
		product_details['name'] = product.name
		product_details['price'] = product.price
		product_details['image'] = product_image
		product_details['quantity'] = item.quantity

		form = Quantity(initial={'quantity': product_details['quantity']})
		product_details['form'] = form

		context['product'].append(product_details)
	# update button
	if request.method == "POST":
		form = Quantity(request.POST)
		if form.is_valid():
			new_quantity = form.cleaned_data.get('quantity')
			product_id = request.POST.get("product_token")
			cart = Sale.objects.get(user_id=session_user, checkout=False)
			cart_item = SaleItem.objects.get(sale=cart, product=product_id)

			# if new quantity equals 0 remove it from SaleItem
			if new_quantity == 0:
				cart_item.delete()
				messages.info(request, f"Item removed from your cart successfully.")
				return redirect(cart_view)
			# stock suffecient and new quantity not equal 0
			elif new_quantity < stock_count(product_id):
				request.session["item_total"] -= cart_item.quantity
				cart_item.quantity = new_quantity
				cart_item.save()
				request.session["item_total"] += new_quantity
				messages.info(request, f"Item quantity updates successfully.")
				return redirect(cart_view)
			else:
				messages.info(request, f"Invalid quantity.")

	return render(request, "cart.html", context)



def checkout(request):
	session_user = request.user.id
	cart = Sale.objects.get(user_id=session_user, checkout=False)
	cart.checkout = True
	cart.save()
	request.session["item_total"] = 0

	return render(request, "checkout.html", context={'user': request.user.first_name})
