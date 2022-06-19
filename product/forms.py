from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from product.models import Product


class Quantity(forms.Form):
    quantity = forms.IntegerField(initial=1)
