from django.db import models
from django.forms import CharField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    SKU = models.PositiveIntegerField()
    price = models.FloatField()
    currency = models.CharField(max_length=20, default='US Dollars')
    description = models,CharField()

    def __str__(self):
        return f"{self.name} - {self.SKU}"

   
# multivalued attribute
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='id')
    image = models.ImageField()
