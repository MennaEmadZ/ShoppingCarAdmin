from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from user.models import BillingAddress, Profile, ShippingAddress
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'user'

class BillingAddressInline(admin.StackedInline):
    model = BillingAddress
    can_delete = False
    verbose_name_plural = 'Billing address'

class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    can_delete = False
    verbose_name_plural = 'shipping address'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, BillingAddressInline, ShippingAddressInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)