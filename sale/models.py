from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from product.models import Product
from user.models import User
# Create your models here.

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id' )
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.id}"


        
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='id')
    quantity = models.IntegerField()
   
    def __str__(self):
        return f"{self.sale}-{self.product}"
    
    def clean(self):
        # check the stock availability.
        if (self.product.stock_count() - self.quantity) <= 0:
            raise ValidationError(('Out of stock.'))
            
        
    