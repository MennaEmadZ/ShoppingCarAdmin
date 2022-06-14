from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models import Sum


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    SKU = models.CharField(unique=True, max_length=70)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    description = models.CharField(max_length=100, default='no description')

    def __str__(self):
        return f"{self.name}"

    def stock_count(self):
        
        purchase = self.purchaseitem_set.all().aggregate(Sum('quantity'))["quantity__sum"]
        sale = self.saleitem_set.all().aggregate(Sum('quantity'))["quantity__sum"]
        # no purchase ans sale yet
        if not purchase and not sale:
            return 0
        # there is a stock but no sale yet  
        elif not sale:
            return purchase
        # there is one or more purchase and sale 
        else:
            return purchase-sale


# multivalued attribute
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='id')
    image = models.ImageField()
