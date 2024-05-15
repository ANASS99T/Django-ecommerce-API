from django.db import models
from order.models import Order

class Shipping(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    # add any additional fields here