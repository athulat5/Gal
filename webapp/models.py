from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    customer=models.OneToOneField(User,on_delete=models.CASCADE)

class Seller(models.Model):
     seller=models.OneToOneField(User,on_delete=models.CASCADE)
    
