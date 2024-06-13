from django.db import models
from django.utils import timezone

from currency.models import Currency
from user.models import Client


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    shipping_address = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('SHIPPED', 'Shipped'),
            ('DELIVERED', 'Delivered'),
            ('CANCELLED', 'Cancelled'),
            ('COMPLETE', 'Complete'),
            ('DELETED', 'Deleted')
        ],
        default='PENDING',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.status = 'DELETED'
        self.save()
