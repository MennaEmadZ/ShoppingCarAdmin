from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile, BillingAddress, ShippingAddress


class RegistrationForm(UserCreationForm):
	first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={"placeholder": "FIRST NAME"}))
	last_name = forms.CharField(label="Last name", widget=forms.TextInput(attrs={"placeholder": "LAST NAME"}))
	username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"placeholder": "USERNAME"}))
	email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"placeholder": "EMAIL ADDRESS"}))

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		exclude = ['user']


class BillingAddressForm(ModelForm):
	class Meta:
		model = BillingAddress
		exclude = ['user']


class ShippingAddressForm(ModelForm):
	class Meta:
		model = ShippingAddress
		exclude = ['user']
