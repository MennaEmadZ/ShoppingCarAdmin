from django.contrib import admin
from django.db.models import F, ExpressionWrapper, DecimalField
from sale.models import Sale, SaleItem
class SaleAdmin(admin.ModelAdmin):
    # a list of readonly columns name.
    readonly_fields = ('date',)

class SaleItemAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['product', 'calculated_total']
    
    def calculated_total(self, obj):
        return obj.total
    calculated_total.admin_order_field = 'total'

    def get_queryset(self, request):
            qs = super(SaleItemAdmin, self).get_queryset(request)
            qs = qs.annotate(total=ExpressionWrapper(F('price')*F('quantity'), output_field=DecimalField())).order_by('total')
            return qs

# Register your models here.
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem, SaleItemAdmin)
