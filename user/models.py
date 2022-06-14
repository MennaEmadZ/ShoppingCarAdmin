from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

# not sure if it right to have the addresses
# in two separete tables
# or merge them and add identification column


# composite attribute
class BillingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, to_field='id')
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    

# composite attribute
class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, to_field='id')
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
