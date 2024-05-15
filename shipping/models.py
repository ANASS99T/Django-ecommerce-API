from django.db import models
from django.utils import timezone
from order.models import Order


class Shipping(models.Model):
    order = models.OneToOneField(
        'order.Order', on_delete=models.CASCADE, related_name='shipping')

    address = models.CharField(max_length=200)
    method = models.CharField(max_length=20, choices=[(
        'STANDARD', 'Standard'), ('EXPRESS', 'Express'), ('OVERNIGHT', 'Overnight')])
    tracking_number = models.CharField(max_length=50, null=True, blank=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()
