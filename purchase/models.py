from django.db import models
from django.utils import timezone
from product.models import Product
from user.models import User


# Create your models here.
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    date = models.DateField(default=timezone.now)   
    def __str__(self):
        return f"{self.id}" 
              
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, to_field='id')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='id')
    quantity = models.IntegerField()
   
    def __str__(self):
        return f"{self.id}-{self.product}"

