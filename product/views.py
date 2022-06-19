from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render

from product.forms import Quantity
from product.models import Product, ProductImage
from purchase.models import PurchaseItem
from sale.models import SaleItem, Sale
# helper function


def stock_count(product):
    purchase_total = PurchaseItem.objects.filter(product=product).aggregate(Sum('quantity'))["quantity__sum"]
    sale_total = SaleItem.objects.filter(product=product).aggregate(Sum('quantity'))["quantity__sum"]
    if not purchase_total:
        return 'Out of stock'
    elif not sale_total:
        return purchase_total
    else:
        return purchase_total - sale_total


# helper function
def cart_helper(user, product, quantity):
    order, created = Sale.objects.get_or_create(user_id=user, checkout=False)
    order_item = SaleItem(sale=order, product_id=product, quantity=quantity)
    order_item.save()


# Create your views here.
def product_details(request, product_id):
    context = dict()
    if request.user.is_authenticated:
        session_user = request.user.id
        context['session_user'] = session_user

    product = Product.objects.get(id=product_id)
    context['product_info'] = product
    context['stock_count'] = stock_count(product_id)
    images = ProductImage.objects.filter(product=product_id)
    context['product_images'] = images

    if request.method == 'POST':
        form = Quantity(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            if context['stock_count'] > quantity:
                cart_helper(user=context['session_user'], product=product.id, quantity=quantity)
                messages.info(request, f"Item added to the cart.")
                request.session["item_total"] += quantity
            else:
                messages.info(request, f"Invalid item quantity.")
    else:
        form = Quantity()
    context['form'] = form
    return render(request, "product_details.html", context)
