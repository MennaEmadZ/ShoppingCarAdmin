from django.contrib import admin

from purchase.models import Purchase, PurchaseItem


class PurchaseAdmin(admin.ModelAdmin):
    # a list of readonly columns name.
    readonly_fields = ('date',)


# Register your models here.
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseItem)
