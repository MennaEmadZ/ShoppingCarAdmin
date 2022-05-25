from django.db import models
from django.contrib import admin
from django.utils import timezone
from product.models import Product
from user.models import User
from django.db.models.functions import Concat
from django.db.models import Value
# Create your models here.

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id' )
    date = models.DateField(default=timezone.now)
    

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='id')
    quantity = models.DecimalField(max_digits=9,  decimal_places=1, default=1)
    price =  models.DecimalField(max_digits=9,  decimal_places=1, default=1)

    def _get_total(self):
                #functions to calculate whatever you want...
                return float(self.product.SKU) - float(self.quantity)
    
    #Register the function to the property method
    # total_price = property(_get_total)
    # class Meta:
    #         ordering = ['total_price']
    # #currency symbol is static for now
    # @admin.display(ordering=Concat(Value('$'), 'total_price'))
    # def full_name(self):
    #     return self.total_price 