from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    customer=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.customer.username

class Seller(models.Model):
     seller=models.OneToOneField(User,on_delete=models.CASCADE)
     def __str__(self):
        return self.seller.username
     
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}'s Cart"