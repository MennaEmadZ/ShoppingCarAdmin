from django.contrib import admin
from sale.models import Sale, SaleItem
from django.db.models import F
class SaleAdmin(admin.ModelAdmin):
    # a list of readonly columns name.
    list_display = ['user', 'calculated_total']
    readonly_fields = ('date',)



    def calculated_total(self, obj):
        #to handle multiple querysets
        sum=0
        total = SaleItem.objects.filter(sale_id=obj.id).annotate(total=F('product__price') * F('quantity'))
        for val in total:
            sum+=val.total
        return sum
        

class SaleItemAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['product',  'quantity']
    
    

# Register your models here.
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem, SaleItemAdmin)
