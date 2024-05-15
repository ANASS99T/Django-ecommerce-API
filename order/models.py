from django.db import models
from product.models import Product
from user.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    # add any additional fields herefrom django.db import models

# Create your models here.
