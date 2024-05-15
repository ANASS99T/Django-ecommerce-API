from django.db import models
from category.models import Category

class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    # add any additional fields here

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)

class ProductVideo(models.Model):
    product = models.OneToOneField(Product, related_name='video', on_delete=models.CASCADE)
    video = models.FileField(upload_to='products/')

class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)