from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(
        max_length=12,
        validators=[
            EmailValidator(
                message="Please enter a valid mail address",
                code="Invalid Email",
            )
        ],
    )
    phone = models.CharField(max_length=20)


# not sure it right to have the addresses 
# in two separete tables
# or merge them and add identification column 

# composite attribute
class BillingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, to_field='id')
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.PositiveIntegerField()

# composite attribute
class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, to_field='id')
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.PositiveIntegerField()

    