from django.contrib import admin
from product.models import Product, ProductImage


class ProductAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['name', 'stock_count']

# Register your models here.


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
